from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from moviesdbapi.models import Movie


class MovieModelTest(TestCase):
    """
    Test class for Movies functional tests
    """

    def setUp(self):
        Movie.objects.create(title='Titanic')

    def test_movie__repr__(self):
        movie = Movie.objects.get(title='Titanic')
        self.assertEqual(movie.__repr__(), 'Movie: Titanic')


client = Client()


class MovieAPITest(TestCase):
    def setUp(self):
        Movie.objects.create(title='Titanic')

    def test_get_200(self):
        response = client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_add_new_movie(self):
    #     data = None
    #     response = client.post(reverse('movie-create'), data)
    #
    #     self.assert