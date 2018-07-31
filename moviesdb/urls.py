from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from moviesdbapi import views

urlpatterns = [
    url(r'^movies', views.MovieList.as_view(), name="movie-list"),
    path(r'comments', views.CommentList.as_view(), name="comment-list"),
    path('admin/', admin.site.urls),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
