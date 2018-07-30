from django.test import TestCase, tag

from moviesdb import settings
from moviesdbapi.providers import OMDBMoviesProvider

EXPECTED_YEAR = 1997
EXPECTED_TITLE = "Titanic"


class OmdbMoviesProviderTest(TestCase):
    @tag('slow')
    def test_fetching_data_from_omdb(self):

        provider = OMDBMoviesProvider()
        movies = provider.find_movies(title=EXPECTED_TITLE)
        self.assertEqual(movies[0].title, EXPECTED_TITLE)
        self.assertEqual(movies[0].year, EXPECTED_YEAR)


