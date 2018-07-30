from django.test import TestCase
from mock import Mock

from moviesdbapi.models import Movie
from moviesdbapi.services import MoviesProvider, MoviesCatalogueService

EXPECTED_YEAR = "1997"
EXPECTED_TITLE = "Titanic"


class MoviesCatalogueServiceTest(TestCase):

    def test_getting_movie_from_external_service(self):
        provider: MoviesProvider = Mock(spec=MoviesProvider)
        provider.find_movies.return_value = [Movie(title=EXPECTED_TITLE, year=EXPECTED_YEAR)]

        mcs = MoviesCatalogueService(provider)
        titanic = mcs.find_first(title=EXPECTED_TITLE)

        self.assertEqual(titanic.year, EXPECTED_YEAR)

    def test_returning_none_if_movie_was_not_found(self):
        provider: MoviesProvider = Mock(spec=MoviesProvider)
        provider.find_movies.return_value = None

        mcs = MoviesCatalogueService(provider)
        self.assertIsNone(mcs.find_first(EXPECTED_TITLE))

    def test_returning_none_if_movie_was_not_found_by_empty_list(self):
        provider: MoviesProvider = Mock(spec=MoviesProvider)
        provider.find_movies.return_value = []

        mcs = MoviesCatalogueService(provider)
        self.assertIsNone(mcs.find_first(EXPECTED_TITLE))

    def test_getting_movie_from_external_service_throws_assertion_error_when_title_is_empty(self):
        provider: MoviesProvider = Mock(spec=MoviesProvider)
        provider.find_movies.return_value = Movie(title=EXPECTED_TITLE, year=EXPECTED_YEAR)

        with self.assertRaises(AssertionError):
            mcs = MoviesCatalogueService(provider)
            # noinspection PyTypeChecker
            mcs.find_first(title=None)  # None passed by purpose


