from unittest import skip

from django.test import TestCase, tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from moviesdbapi.models import Movie
from moviesdbapi.serializers import MovieSerializer, CommentSerializer

EMPTY_BODY = ""

EXISTING_MOVIE_TITLE = 'Inception'
EXISTING_MOVIE_YEAR = 2010
ANOTHER_EXISTING_MOVIE_TITLE = 'Titanic'
NOT_EXISTING_MOVIE_TITLE = 'Live of Wojtek from Samsung'

ANY_MOVIE_ID = 1
NOT_EXISTING_MOVIE_ID = 999
EXAMPLE_COMMENT_BODY = "Save the 418!"

client = APIClient()


class MovieAPITest(TestCase):
    @tag('slow')
    def test_get_empty_movie_list(self):
        response = client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    @tag('slow')
    def test_list_two_movies_after_adding_two_movies(self):
        client.post(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE}, format='json')
        client.post(reverse('movie-list'), data={'title': ANOTHER_EXISTING_MOVIE_TITLE}, format='json')

        response = client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @tag('slow')
    def test_list_filtered_movie_by_title(self):
        client.post(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE}, format='json')
        client.post(reverse('movie-list'), data={'title': ANOTHER_EXISTING_MOVIE_TITLE}, format='json')

        response = client.get(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @tag('slow')
    def test_list_filtered_movie_by_year(self):
        client.post(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE}, format='json')
        client.post(reverse('movie-list'), data={'title': ANOTHER_EXISTING_MOVIE_TITLE}, format='json')

        response = client.get(reverse('movie-list'), data={'year': EXISTING_MOVIE_YEAR})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @tag('slow')
    def test_list_filtered_movie_by_year_and_title(self):
        client.post(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE}, format='json')
        client.post(reverse('movie-list'), data={'title': ANOTHER_EXISTING_MOVIE_TITLE}, format='json')

        response = client.get(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE, 'year': EXISTING_MOVIE_YEAR})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @tag('slow')
    def test_list_filtered_movie_found_none(self):
        client.post(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE}, format='json')
        client.post(reverse('movie-list'), data={'title': ANOTHER_EXISTING_MOVIE_TITLE}, format='json')

        response = client.get(reverse('movie-list'), data={'title': NOT_EXISTING_MOVIE_ID})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 0)

    @tag('slow')
    def test_list_filtered_movie_by_invalid_field_ignores_filters(self):
        client.post(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE}, format='json')
        client.post(reverse('movie-list'), data={'title': ANOTHER_EXISTING_MOVIE_TITLE}, format='json')

        response = client.get(reverse('movie-list'), data={'foo': 'bar'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 2)

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


class CommentsAPITest(TestCase):
    """
    POST /comments:
    Request body should contain ID of movie already present in database, and comment text body.
    Comment should be saved to application database and returned in request response.

    GET /comments:
    Should fetch list of all comments present in application database.
    Should allow filtering comments by associated movie, by passing its ID.
    """

    @tag('slow')
    def test_adding_new_comment(self):
        movie_response = client.post(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE}, format='json')
        response = client.post(reverse('comment-list'),
                               data={'movie': movie_response.data['id'], 'body': EXAMPLE_COMMENT_BODY})

        serializer = CommentSerializer(data=response.data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(serializer.is_valid())

    @tag('slow')
    def test_adding_new_comment_to_non_existing_movie(self):
        response = client.post(reverse('comment-list'),
                               data={'movie': NOT_EXISTING_MOVIE_ID, 'body': EXAMPLE_COMMENT_BODY})

        serializer = CommentSerializer(data=response.data)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(serializer.is_valid())

    @tag('slow')
    def test_adding_new_comment_with_empty_body(self):
        response = client.post(reverse('comment-list'),
                               data={'movie': ANY_MOVIE_ID, 'body': EMPTY_BODY})

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag('slow')
    def test_fetch_empty_comments_list(self):
        response = client.get(reverse('comment-list'))

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.data, [])

    @tag('slow')
    def test_list_two_comments_after_adding_two_comments(self):
        response = client.post(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE}, format='json')

        client.post(reverse('comment-list'), data={'movie': response.data['id'], 'body': EXAMPLE_COMMENT_BODY})
        client.post(reverse('comment-list'), data={'movie': response.data['id'], 'body': EXAMPLE_COMMENT_BODY})

        response = client.get(reverse('comment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @tag('slow')
    def test_filter_list_of_comments_by_movie_id(self):
        response_1 = client.post(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE}, format='json')
        response_2 = client.post(reverse('movie-list'), data={'title': ANOTHER_EXISTING_MOVIE_TITLE}, format='json')

        client.post(reverse('comment-list'), data={'movie': response_1.data['id'], 'body': EXAMPLE_COMMENT_BODY})
        client.post(reverse('comment-list'), data={'movie': response_2.data['id'], 'body': EXAMPLE_COMMENT_BODY})

        response = client.get(reverse('comment-list'), data={'movie': response_1.data['id']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @tag('slow')
    def test_filter_list_of_comments_by_not_existing_movie_id(self):
        response_1 = client.post(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE}, format='json')
        response_2 = client.post(reverse('movie-list'), data={'title': ANOTHER_EXISTING_MOVIE_TITLE}, format='json')

        client.post(reverse('comment-list'), data={'movie': response_1.data['id'], 'body': EXAMPLE_COMMENT_BODY})
        client.post(reverse('comment-list'), data={'movie': response_2.data['id'], 'body': EXAMPLE_COMMENT_BODY})

        response = client.get(reverse('comment-list'), data={'movie': NOT_EXISTING_MOVIE_ID})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    @tag('slow')
    def test_filter_list_of_comments_by_empty_movie_id(self):
        response_1 = client.post(reverse('movie-list'), data={'title': EXISTING_MOVIE_TITLE}, format='json')
        response_2 = client.post(reverse('movie-list'), data={'title': ANOTHER_EXISTING_MOVIE_TITLE}, format='json')

        client.post(reverse('comment-list'), data={'movie': response_1.data['id'], 'body': EXAMPLE_COMMENT_BODY})
        client.post(reverse('comment-list'), data={'movie': response_2.data['id'], 'body': EXAMPLE_COMMENT_BODY})

        response = client.get(reverse('comment-list'), data={'movie': ""})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
