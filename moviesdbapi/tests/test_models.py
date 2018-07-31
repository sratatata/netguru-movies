from django.test import TestCase

from moviesdbapi.models import Movie, Comment


class MovieModelTest(TestCase):
    """
    Test class for Movies model test.
    """

    def setUp(self):
        Movie.objects.create(title='Titanic', year=2010)

    def test_movie__repr__(self):
        movie = Movie.objects.get(title='Titanic')
        self.assertEqual(movie.__repr__(), 'Movie: Titanic from 2010')


class CommentModelTest(TestCase):
    """
    Test class for Comment model test.
    """

    def setUp(self):
        movie = Movie.objects.create(title='Titanic', year=2010)
        Comment.objects.create(movie=movie, body="Awesome!")

    def test_comment__repr__(self):
        comment = Comment.objects.all().first()
        self.assertEqual(comment.__repr__(), 'Comment to Titanic: Awesome!')


