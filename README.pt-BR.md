<p align="center">
  <img src="source/img/logo.png" alt="Botflix" width="220">
</p>

<h1 align="center">Botflix</h1>

<p align="center">
  Um bot do Telegram para pesquisar filmes e séries usando a API do OMDb.
</p>

<p align="center">
  <a href="README.md">🇺🇸 English</a> | 🇧🇷 Português
</p>

## Sobre o projeto

O **Botflix** é um bot do Telegram que permite pesquisar filmes e séries direto na conversa. As informações vêm da [OMDb API](https://www.omdbapi.com/), que fornece dados como título, ano, sinopse, elenco e nota.

O bot terá suporte a dois idiomas, português e inglês (arquivos em [source/locale/](source/locale/)).

> 🚧 Projeto em desenvolvimento.

## Tecnologias

- Python
- FastAPI
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [OMDb API](https://www.omdbapi.com/)

## Como rodar

1. Clone o repositório e instale as dependências:

   ```bash
   git clone https://github.com/ftfariasdev/Botflix.git
   cd Botflix
   pip install -r requirements.txt
   ```

2. Copie o arquivo de exemplo e preencha com os seus tokens:

   ```bash
   cp .env.example .env
   ```

   | Variável     | Descrição                                           |
   | ------------ | --------------------------------------------------- |
   | `TG_TOKEN`   | Token do bot, obtido com o [@BotFather](https://t.me/BotFather) |
   | `OMDB_TOKEN` | Chave da API, obtida em [omdbapi.com](https://www.omdbapi.com/apikey.aspx) |

3. Inicie a aplicação:

   ```bash
   uvicorn main:app --reload
   ```
