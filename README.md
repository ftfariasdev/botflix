<p align="center">
  <img src="source/img/logo.png" alt="Botflix" width="220">
</p>

<h1 align="center">Botflix</h1>

<p align="center">
  A Telegram bot that searches movies and TV series using the OMDb API.
</p>

<p align="center">
  🇺🇸 English | <a href="README.pt-BR.md">🇧🇷 Português</a>
</p>

## About

**Botflix** is a Telegram bot that lets you search for movies and TV series right from the chat. The data comes from the [OMDb API](https://www.omdbapi.com/), which provides details such as title, year, plot, cast and rating.

The bot will support two languages, English and Portuguese (files in [source/locale/](source/locale/)).

> 🚧 Work in progress.

## Tech stack

- Python
- FastAPI
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [OMDb API](https://www.omdbapi.com/)

## Getting started

1. Clone the repository and install the dependencies:

   ```bash
   git clone https://github.com/ftfariasdev/Botflix.git
   cd Botflix
   pip install -r requirements.txt
   ```

2. Copy the example file and fill in your tokens:

   ```bash
   cp .env.example .env
   ```

   | Variable     | Description                                                              |
   | ------------ | ------------------------------------------------------------------------ |
   | `TG_TOKEN`   | Bot token, obtained from [@BotFather](https://t.me/BotFather)            |
   | `OMDB_TOKEN` | API key, obtained at [omdbapi.com](https://www.omdbapi.com/apikey.aspx)  |

3. Start the application:

   ```bash
   uvicorn main:app --reload
   ```
