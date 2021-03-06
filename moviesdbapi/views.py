from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from moviesdbapi.models import Movie, Comment
from moviesdbapi.providers import OMDBMoviesProvider
from moviesdbapi.serializers import MovieSerializer, CommentSerializer
from moviesdbapi.services import MoviesCatalogueService
from moviesdbapi.views_helpers import generic_filter_by_query_parameters, generic_sort


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

        movies = generic_filter_by_query_parameters(movies, request, ignored=['sort_by', 'order'])
        movies = generic_sort(movies, request)

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if 'title' in request.data:
            title = request.data['title']
            movie = self.movies_catalogue.find_first(title)

            # Serialize and later serialize to make sure that
            # movie is in proper format. I rather like this than returning dict from service
            json = MovieSerializer(movie).data  # TODO remove this hack if enough time
            serializer = MovieSerializer(data=json)  # TODO remove this hack if enough time

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Missing title value", status=status.HTTP_400_BAD_REQUEST)


class CommentList(APIView):
    """
    API endpoint that allow posting or viewing comments
    """

    def get(self, request, format=None):
        comments = Comment.objects.all()
        filter_by_movie_id = request.query_params.get('movie', None)
        if filter_by_movie_id:
            comments = comments.filter(movie=filter_by_movie_id)
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


