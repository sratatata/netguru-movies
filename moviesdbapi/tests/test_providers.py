from django.test import TestCase, tag

from moviesdb import settings
from moviesdbapi.providers import OMDBMoviesProvider

EXPECTED_YEAR = "1997"
EXPECTED_TITLE = "Titanic"
NOT_EXISTING_MOVIE_TITLE = 'Live of Wojtek from Samsung'


class OmdbMoviesProviderTest(TestCase):
    @tag('slow')
    def test_fetching_data_from_omdb(self):

        provider = OMDBMoviesProvider()
        movies = provider.find_movies(title=EXPECTED_TITLE)
        self.assertEqual(movies[0].title, EXPECTED_TITLE)
        self.assertEqual(movies[0].year, EXPECTED_YEAR)

    @tag('slow')
    def test_fetching_data_from_omdb_for_non_existing_movie(self):
        provider = OMDBMoviesProvider()
        movies = provider.find_movies(title=NOT_EXISTING_MOVIE_TITLE)
        self.assertIsNone(movies)


