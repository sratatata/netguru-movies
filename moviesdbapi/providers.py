from abc import ABCMeta, abstractmethod
from typing import List, Optional

import requests
from rest_framework import status

from moviesdb import settings
from moviesdbapi.models import Movie

URL = 'http://www.omdbapi.com/'


class MoviesProvider(metaclass=ABCMeta):
    """
    MoviesProvider is an abstract class which should be exactly implemented
    by any of implementors so MoviesCatalogueService which depends on
    MoviesProviders could work seamlessly.
    """

    @abstractmethod
    def find_movies(self, title: str) -> Optional[List[Movie]]:
        """
        Search for movies by title.
        :param title:
        :return: List of matching movies or None if no movies found.
        """
        raise NotImplementedError("Abstract method")


class OMDBMoviesProvider(MoviesProvider):
    def __init__(self, api_key=None):
        """
        OMDB service needs api_key which could be obtained from their website.
        If api_key is not provided via __init__ method, it would be loaded from
        django settings.py.

        :param api_key: see http://www.omdbapi.com
        """
        if api_key:
            self.api_key = api_key
        else:
            self.__load_secret()

    def find_movies(self, title: str) -> Optional[List[Movie]]:
        response = requests.get(URL, params={'t': title, 'apikey': self.api_key})
        assert response.status_code == status.HTTP_200_OK

        return self.__parse(response.json())

    @staticmethod
    def __parse(json) -> Optional[List[Movie]]:
        """
        Manual deserialization of record from OMDB rest api.
        (possible improvement, by providing deserializer)
        :param json: native OMDB json response
        :return: Movie model instance in role of DTO (possible improvement use actual DTO pattern and map to model in service)
        """
        # TODO <--- for sake of simplicity I'm omitting schema validation, which should be always
        # TODO tested when external services are called for value
        try:
            movie = Movie()
            movie.title = json["Title"]
            movie.year = int(json["Year"])
            return [movie]
        except KeyError:
            return None

    def __load_secret(self):
        # TODO: Not sure if it's proper way of handling settings in Django, but it's simple and works
        # TODO: Please refactor if better way is optimal
        self.api_key = settings.OMDB_SECRET
        assert self.api_key, "Provide OMDB_SECRET in settings.py"
