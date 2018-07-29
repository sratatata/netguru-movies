from rest_framework import viewsets

from moviesdbapi.models import Movie
from moviesdbapi.serializers import MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows movies to be viewed or edited.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
