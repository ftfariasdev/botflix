import os
import time
import requests
from dotenv import load_dotenv
from i18n import normalize_lang, t

load_dotenv("../.env")

API_URL = f"https://api.telegram.org/bot{os.getenv('TG_TOKEN')}"

# Armazena o idioma escolhido por cada usuário
user_languages = {}


def get_main_menu_keyboard(lang):
    ## """Retorna o teclado principal no idioma especificado."""
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
        # 1. Identifica se a atualização é uma mensagem de texto
        if "message" in update:
            message = update["message"]
            text = message.get("text", "")
            user = message.get("from", {})
            chat_id = message.get("chat", {}).get("id")
            user_id = user.get("id")

            lang = user_languages.get(
                user_id, normalize_lang(user.get("language_code"))
            )

            # Menu de seleção de idioma via comando
            if text == "/language" or text == t("OPTIONS.SELECT_LANGUAGE", lang):
                requests.post(
                    f"{API_URL}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": t("OPTIONS.SELECT_LANGUAGE", lang),
                        "reply_markup": get_language_keyboard(lang),
                    },
                    timeout=2,
                )
            else:
                welcome = t("WELCOME", lang, username=user.get("first_name", ""))
                requests.post(
                    f"{API_URL}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": welcome,
                        "reply_markup": get_main_menu_keyboard(lang),
                    },
                    timeout=2,
                )

        # 2. Identifica quando o usuário clica em um botão inline
        elif "callback_query" in update:
            callback = update["callback_query"]
            user = callback.get("from", {})
            user_id = user.get("id")
            chat_id = callback.get("message", {}).get("chat", {}).get("id")
            data = callback.get("data")

            lang = user_languages.get(
                user_id, normalize_lang(user.get("language_code"))
            )

            # Caso o usuário clique no botão "Pesquisar filme" do menu principal
            if data == "movie":
                requests.post(
                    f"{API_URL}/sendMessage",
                    json={
                        "text": t("MOVIE.COMING_SOON", lang),
                        "chat_id": chat_id,
                        "reply_markup": get_main_menu_keyboard(lang)
                    },
                    timeout=2,
                )

            # Caso o usuário clique no botão "Idioma" do menu principal
            if data == "language":
                requests.post(
                    f"{API_URL}/answerCallbackQuery",
                    json={"callback_query_id": callback["id"]},
                    timeout=2,
                )
                if chat_id:
                    requests.post(
                        f"{API_URL}/sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": t("OPTIONS.SELECT_LANGUAGE", lang),
                            "reply_markup": get_language_keyboard(lang),
                        },
                        timeout=2,
                    )

            # Caso o usuário escolha "pt" ou "en"
            elif data in ["pt", "en"]:
                user_languages[user_id] = data

                requests.post(
                    f"{API_URL}/answerCallbackQuery",
                    json={
                        "callback_query_id": callback["id"],
                        "text": (
                            "Idioma selecionado!"
                            if data == "pt"
                            else "Language selected!"
                        ),
                    },
                    timeout=2,
                )

                welcome = t("WELCOME", data, username=user.get("first_name", ""))
                if chat_id:
                    requests.post(
                        f"{API_URL}/sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": welcome,
                            "reply_markup": get_main_menu_keyboard(data),
                        },
                        timeout=2,
                    )


# Controla quais atualizações já foram processadas
offset = None
print("Bot iniciado! Aguardando mensagens...")

# Mantém o bot funcionando continuamente
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
                try:
                    verification_message({"ok": True, "result": [update]})
                except Exception as erro:
                    print(f"Erro ao processar atualização: {erro}")
                finally:
                    offset = update["update_id"] + 1

    except requests.exceptions.RequestException as erro:
        print(f"Erro de conexão com Telegram: {erro}")
        time.sleep(3)
    except Exception as erro:
        print(f"Erro inesperado: {erro}")
        time.sleep(3)
