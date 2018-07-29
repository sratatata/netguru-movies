from rest_framework import serializers

from moviesdbapi.models import Movie


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'year')
