from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from moviesdbapi.models import Movie
from moviesdbapi.serializers import MovieSerializer


class MovieModelTest(TestCase):
    """
    Test class for Movies functional tests
    """

    def setUp(self):
        Movie.objects.create(title='Titanic')

    def test_movie__repr__(self):
        movie = Movie.objects.get(title='Titanic')
        self.assertEqual(movie.__repr__(), 'Movie: Titanic')


client = APIClient()


class MovieAPITest(TestCase):
    def setUp(self):
        Movie.objects.create(title='Titanic')

    def test_get_200(self):
        response = client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_new_movie(self):
        response = client.post(reverse('movie-list'), data={'title': 'Inception'}, format='json')

        movies = Movie.objects.all()
        inception = movies.get(title='Inception')

        # new movie added
        self.assertEqual(movies.count(), 2)
        self.assertEqual(inception.title, 'Inception')

        # response object is valid
        serializer = MovieSerializer(data=response.data)
        self.assertTrue(serializer.is_valid())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)