from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from moviesdbapi import views

router = routers.DefaultRouter()
router.register(r'movies', views.MovieViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
