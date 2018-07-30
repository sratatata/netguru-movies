from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from moviesdbapi.models import Movie
from moviesdbapi.providers import OMDBMoviesProvider
from moviesdbapi.serializers import MovieSerializer
from moviesdbapi.services import MoviesCatalogueService


class MovieList(APIView):
    """
    API endpoint that allows movies to be viewed or edited.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        provider = OMDBMoviesProvider()  # top level in django application, so doesn't bother to inject
        self.movies_catalogue = MoviesCatalogueService(
            provider)  # top level in django application, so doesn't bother to inject

    def get(self, request, format=None):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if 'title' in request.data:
            title = request.data['title']
            movie = self.movies_catalogue.find_first(title)

            # Serialize and later serialize to make sure that
            # movie is in proper format. I rather like this than returning dict from service
            json = MovieSerializer(movie).data  # TODO remove this hack if enough time
            serializer = MovieSerializer(data=json)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Missing title value", status=status.HTTP_400_BAD_REQUEST)
