from abc import ABCMeta, abstractmethod
from typing import List

import requests
from rest_framework import status

from moviesdb import settings
from moviesdbapi.models import Movie


class MoviesProvider(metaclass=ABCMeta):
    @abstractmethod
    def find_movies(self, title: str) -> List[Movie]:
        raise NotImplementedError("Abstract method")


class OMDBMoviesProvider(MoviesProvider):
    def __init__(self, api_key=None):
        if api_key:
            self.api_key = api_key
        else:
            self.__load_secret()

    def find_movies(self, title: str) -> List[Movie]:
        response = requests.get('http://www.omdbapi.com/', params={'t': title, 'apikey': self.api_key})
        assert response.status_code == status.HTTP_200_OK

        return self.__parse(response.json())

    @staticmethod
    def __parse(json) -> List[Movie]:
        # TODO <--- for sake of simplicity I'm omitting schema validation, which should be always
        # TODO tested when external services are called for value
        movie = Movie()
        movie.title = json["Title"]
        movie.year = int(json["Year"])
        return [movie]

    def __load_secret(self):
        # TODO: Not sure if it's proper way of handling settings in Django, but it's simple and works
        # TODO: Please refactor if better way is optimal
        self.api_key = settings.OMDB_SECRET
        assert self.api_key, "Provide OMDB_SECRET in settings.py"
