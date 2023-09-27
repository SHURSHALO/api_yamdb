from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, GenreViewSet, CategoryViewSet

router_v1 = DefaultRouter()
router_v1.register(r'titles', TitleViewSet),
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
