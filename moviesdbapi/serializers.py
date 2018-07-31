from rest_framework import serializers

from moviesdbapi.models import Movie, Comment


class MovieSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'year')


class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'movie', 'body')
