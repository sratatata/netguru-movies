from rest_framework import status
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

    def post(self, request, format=None):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
