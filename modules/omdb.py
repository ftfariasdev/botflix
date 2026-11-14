import os
from dotenv import load_dotenv
import requests
load_dotenv(".env.example")

def movie_search(movie):
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
# this can and will be changed later to work with the telegram bot.
    if data.get("Response") == "False":
        print("\nMovie not found.")
    else:
        print("Title:", data["Title"])
        print("Year:", data["Year"])
        print("Genre:", data["Genre"])
        print("Plot:", data["Plot"])
        print("IMDB Rating:", data["imdbRating"])

# An example of how it can take a string from somewhere else and use it to search a movie.
print(movie_search("avengers 2019"))