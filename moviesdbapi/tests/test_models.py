from django.test import TestCase

from moviesdbapi.models import Movie


class MovieModelTest(TestCase):
    """
    Test class for Movies model integration test.
    """

    def setUp(self):
        Movie.objects.create(title='Titanic', year=2010)

    def test_movie__repr__(self):
        movie = Movie.objects.get(title='Titanic')
        self.assertEqual(movie.__repr__(), 'Movie: Titanic from 2010')


