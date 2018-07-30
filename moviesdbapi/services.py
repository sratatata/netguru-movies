
from typing import List, Optional

from moviesdbapi.models import Movie
from moviesdbapi.providers import MoviesProvider


class MoviesCatalogueService(object):
    def __init__(self, provider: MoviesProvider):
        """
        Movies catalog service is using provider to fetch movies form internal/external resources.

        :param provider: implementation of MoviesProvider to fetch from
        """
        self.provider = provider

    def find_first(self, title: str) -> Optional[List[Movie]]:
        """
        Search for movie by title and return first movie found.
        (improvement possible for making more deterministic searches)
        :param title: search phrase
        :return: Movie model
        """
        assert title, "Title can't be empty"

        result = self.provider.find_movies(title)
        if result:
            return next((r for r in result))
        else:
            return None
