import os

import requests
from dotenv import load_dotenv

from modules.i18n import t

load_dotenv(".env")
API_URL = f"https://api.telegram.org/bot{os.getenv('TG_TOKEN')}"


def get_updates() -> list[dict]:
    return requests.get(f"{API_URL}/getUpdates").json()["result"]


def send_message(chat_id: int, text: str) -> None:
    requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})


def build_welcome(user: dict) -> str:
    lang = user.get("language_code")  # sent by Telegram, e.g. "pt-br"
    return "\n".join(
        [
            t("WELCOME", lang, username=user.get("first_name", "")),
            t("MENU.OPTION_1", lang),
            t("MENU.OPTION_2", lang),
            t("MENU.CHANGE_LANGUAGE", lang),
        ]
    )


def handle_update(update: dict) -> None:
    message = update.get("message")
    if not message:
        return
    send_message(message["chat"]["id"], build_welcome(message["from"]))


if __name__ == "__main__":
    updates = get_updates()
    if updates:
        handle_update(updates[-1])
