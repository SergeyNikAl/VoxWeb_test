from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, NewsViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('news', NewsViewSet, basename='news')

urlpatterns = [
    path('', include(router_v1.urls)),
]