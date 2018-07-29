from rest_framework.response import Response
from rest_framework.views import APIView

from moviesdbapi.models import Movie
from moviesdbapi.serializers import MovieSerializer


class MovieList(APIView):
    """
    API endpoint that allows movies to be viewed or edited.
    """

    def get(self, request, format=None):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
