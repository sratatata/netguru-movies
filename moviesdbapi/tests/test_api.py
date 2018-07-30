from unittest import skip

from django.test import TestCase, tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from moviesdbapi.models import Movie
from moviesdbapi.serializers import MovieSerializer

EXISTING_MOVIE_TITLE = 'Inception'
NOT_EXISTING_MOVIE_TITLE = 'Live of Wojtek from Samsung'

client = APIClient()


class MovieAPITest(TestCase):
    @tag('slow')
    def test_get_200(self):
        response = client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @tag('slow')
    def test_add_new_movie(self):
        response = client.post(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE}, format='json')

        movies = Movie.objects.all()
        inception = movies.get(title=EXISTING_MOVIE_TITLE)

        # new movie added
        self.assertEqual(movies.count(), 1)
        self.assertEqual(inception.title, EXISTING_MOVIE_TITLE)

        # response object is valid
        serializer = MovieSerializer(data=response.data)
        self.assertTrue(serializer.is_valid())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @tag('slow')
    def test_invalid_body_when_adding_new_movie(self):
        response = client.post(reverse('movie-list'), data={'invalid': 'field'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('slow')
    def test_new_movie_is_fetched_from_external_api(self):
        response = client.post(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE}, format='json')
        serializer = MovieSerializer(data=response.data)

        self.assertTrue(serializer.is_valid())

        inception = Movie.objects.get(title='Inception')
        serializer2 = MovieSerializer(inception)
        self.assertEqual(response.data, serializer2.data)

    @tag('slow')
    def test_not_existing_movie_is_not_fetched_from_external_api(self):
        response = client.post(reverse('movie-list'), data={'title': NOT_EXISTING_MOVIE_TITLE}, format='json')
        serializer = MovieSerializer(data=response.data)

        self.assertFalse(serializer.is_valid())


