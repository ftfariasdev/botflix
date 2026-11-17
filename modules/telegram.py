import os
import time
import logging
import requests
from dotenv import load_dotenv
from i18n import normalize_lang, t
from omdb import movie_search

load_dotenv()

TOKEN = os.getenv("TG_TOKEN")
API_URL = f"https://api.telegram.org/bot{TOKEN}"

# Stores the language selected by each user
user_languages = {}


# Sends a message to the user
def send_message(chat_id, text, keyboard=None):
    payload = {"chat_id": chat_id, "text": text}
    if keyboard:
        payload["reply_markup"] = keyboard
    requests.post(f"{API_URL}/sendMessage", json=payload, timeout=5)


# Answers an inline button callback
def answer_callback(callback_id, text=None):
    payload = {"callback_query_id": callback_id}
    if text:
        payload["text"] = text
    requests.post(f"{API_URL}/answerCallbackQuery", json=payload, timeout=5)


# Gets the user's language
def get_lang(user):
    return user_languages.get(
        user.get("id"), normalize_lang(user.get("language_code"))
    )


def get_main_menu_keyboard(lang):
    return {
        "inline_keyboard": [
            [
                {"text": t("OPTIONS.MOVIES", lang), "callback_data": "movie"},
                {"text": t("OPTIONS.LANGUAGE", lang), "callback_data": "language"},
            ]
        ]
    }


def get_language_keyboard(lang):
    return {
        "inline_keyboard": [
            [
                {"text": t("LANGUAGES.PORTUGUESE", lang), "callback_data": "pt"},
                {"text": t("LANGUAGES.ENGLISH", lang), "callback_data": "en"},
            ]
        ]
    }


def verification_message(data_updates):
    if not data_updates.get("ok") or not data_updates.get("result"):
        return

    for update in data_updates["result"]:

        # Handles incoming text messages
        if "message" in update:
            message = update["message"]                      
            text = message.get("text", "")                   
            user = message.get("from", {})                   
            chat_id = message.get("chat", {}).get("id")      
            lang = get_lang(user)                            

            reply = message.get("reply_to_message") 
            if reply and reply.get("text") == t("MOVIE.WRITE_MOVIE", lang):
                movie = movie_search(text)
                if not movie:
                    send_message(chat_id, t("ERRORS.INVALID_SEARCH", lang))
                    send_message(chat_id, t("MOVIE.CONTINUE", lang), get_main_menu_keyboard(lang))
                    continue
                send_movie(chat_id, movie, lang)
                continue

            if text == "/language" or text == t("OPTIONS.SELECT_LANGUAGE", lang):   # 79
                send_message(
                    chat_id,
                    t("OPTIONS.SELECT_LANGUAGE", lang),
                    get_language_keyboard(lang)
                )
            else:
                welcome = t("WELCOME", lang, username=user.get("first_name", ""))
                send_message(chat_id, welcome, get_main_menu_keyboard(lang))

        # Handles inline button callbacks
        elif "callback_query" in update:
            callback = update["callback_query"]
            user = callback.get("from", {})
            user_id = user.get("id")
            chat_id = callback.get("message", {}).get("chat", {}).get("id")
            data = callback.get("data")
            lang = get_lang(user)

            answer_callback(
                callback["id"],
                t("LANGUAGES.SELECTED", data) if data in ["pt", "en"] else None
            )

            if data == "movie":
                send_message(
                    chat_id,
                    t("MOVIE.WRITE_MOVIE", lang),
                    {"force_reply": True}
                )

            elif data == "language":
                send_message(
                    chat_id,
                    t("OPTIONS.SELECT_LANGUAGE", lang),
                    get_language_keyboard(lang)
                )

            elif data in ["pt", "en"]:
                user_languages[user_id] = data
                welcome = t("WELCOME", data, username=user.get("first_name", ""))
                send_message(chat_id, welcome, get_main_menu_keyboard(data))

#region Search movies
def format_movie(movie, lang):
    return (
        f"{t('MOVIE_INFO.TITLE', lang)} {movie['Title']}\n"
        f"{t('MOVIE_INFO.YEAR', lang)} {movie['Year']}\n"
        f"{t('MOVIE_INFO.GENRE', lang)} {movie['Genre']}\n"
        f"{t('MOVIE_INFO.RATING', lang)} {movie['imdbRating']}\n"
        f"{t('MOVIE_INFO.PLOT', lang)} {movie['Plot']}"
    )

def send_movie(chat_id, movie, lang):
    texto = format_movie(movie, lang)
    url_poster = movie.get("Poster")

    if url_poster and url_poster != "N/A":
        requests.post(
            f"{API_URL}/sendPhoto",          # use a mesma URL base do seu send_message
            json={"chat_id": chat_id, "photo": url_poster, "caption": texto},
        )
    else:
        send_message(chat_id, texto)
    send_message(chat_id, t("MOVIE.CONTINUE", lang), get_main_menu_keyboard(lang))

def main():
    if not TOKEN:
        raise SystemExit("TG_TOKEN is not defined. Check your .env file.")

    # Tracks processed updates
    offset = None
    logging.basicConfig(level=logging.INFO)
    print("Bot started! Waiting for messages...")

    # Keeps the bot running continuously
    while True:
        try:
            params = {"timeout": 30}
            if offset is not None:
                params["offset"] = offset

            response = requests.get(f"{API_URL}/getUpdates", params=params, timeout=35)
            response.raise_for_status()
            updates = response.json()

            if updates.get("ok"):
                for update in updates["result"]:
                    offset = update["update_id"] + 1
                    try:
                        verification_message({"ok": True, "result": [update]})
                    except Exception:
                        logging.exception("Error processing update")

        except requests.exceptions.RequestException:
            logging.exception("Telegram connection error")
            time.sleep(3)
        except Exception:
            logging.exception("Unexpected error")
            time.sleep(3)


if __name__ == "__main__":
    main()
