import os
import requests
from dotenv import load_dotenv
from i18n import normalize_lang, t

load_dotenv("../.env")
API_URL = f"https://api.telegram.org/bot{os.getenv('TG_TOKEN')}"
updates = requests.get(f"{API_URL}/getUpdates")
updates = updates.json()


def verification_message(data_updates):
    if data_updates.get("ok") and data_updates.get("result"):
        last_update = data_updates["result"][-1]

        message = last_update.get("message", {})
        text = message.get("text", "")
        user = message.get("from", {})
        chat_id = message.get("chat", {}).get("id")

        lang = normalize_lang(user.get("language_code"))
        if text == "/language":
            keyboard = {
                "inline_keyboard": [
                    [
                        {"text": "🇧🇷 Português", "callback_data": "pt"},
                        {"text": "🇺🇸 English", "callback_data": "en"}
                    ]
                ]
            }

            requests.post(
                f"{API_URL}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": "Selecione seu idioma / Select your language:",
                    "reply_markup": keyboard
                }
            )

        else:
            welcome = "\n".join([
                t("WELCOME", lang, username=user.get("first_name", "")),
                t("MENU.OPTION_1", lang),
                t("MENU.OPTION_2", lang),
                t("MENU.CHANGE_LANGUAGE", lang)
            ])

            requests.post(
                f"{API_URL}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": welcome
                }
            )

    else:
        print("Nenhuma mensagem encontrada!")


verification_message(updates)