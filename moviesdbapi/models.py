from django.db import models


class Movie(models.Model):
    """
    Movie model
    Defines the attributes of a movie.
    """

    title = models.CharField(max_length=255)
    year = models.CharField(max_length=30, null=True, blank=True)

    def __repr__(self):
        return f'Movie: {self.title} from {self.year}'


class Comment(models.Model):
    """
    Comment model
    Defines the attributes of comment

    movie_id: id of commented movie
    body: string content of the comment
    """

    body = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, related_name='movie', on_delete=models.CASCADE)

    def __repr__(self):
        return f'Comment to {self.movie.title}: {self.body}'
