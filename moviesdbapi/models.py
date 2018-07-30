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
