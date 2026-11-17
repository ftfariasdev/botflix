import os
from dotenv import load_dotenv
from i18n import t
import requests
load_dotenv(".env")

def movie_search(movie, lang="en"):
    movie_info = movie.rsplit(" ", 1)
    url = "https://www.omdbapi.com/"

    if len(movie_info) == 2 and movie_info[1].isdigit() and len(movie_info[1]) == 4:
        movie = movie_info[0]
        year = movie_info[1]

        response = requests.get(url, params={
            "s": movie,
            "y": year,
            "apikey": os.getenv("OMDB_TOKEN")
        })
        data = response.json()

        if data.get("Response") == "True":
            response = requests.get(url, params={
                "i": data["Search"][0]["imdbID"],
                "apikey": os.getenv("OMDB_TOKEN")
            })
            data = response.json()

    else:
        response = requests.get(url, params={
            "t": movie,
            "apikey": os.getenv("OMDB_TOKEN")
        })
        data = response.json()

    if data.get("Response") == "False":
        return t("ERRORS.INVALID_SEARCH", lang)

    return "\n".join([
        f'{t("MOVIE_INFO.TITLE", lang)} {data["Title"]}',
        f'{t("MOVIE_INFO.YEAR", lang)} {data["Year"]}',
        f'{t("MOVIE_INFO.GENRE", lang)} {data["Genre"]}',
        f'{t("MOVIE_INFO.PLOT", lang)} {data["Plot"]}',
        f'{t("MOVIE_INFO.RATING", lang)} {data["imdbRating"]}',
    ])

# An example of how it can take a string from somewhere else and use it to search a movie.
print(movie_search("avengers 2019"))