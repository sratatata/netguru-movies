
from typing import List, Optional

from moviesdbapi.models import Movie
from moviesdbapi.providers import MoviesProvider


class MoviesCatalogueService(object):

    def __init__(self, provider: MoviesProvider):
        self.provider = provider

    def find_first(self, title: str) -> Optional[List[Movie]]:
        assert title, "Title can't be empty"

        result = self.provider.find_movies(title)
        if result:
            return next((r for r in result))
        else:
            return None
