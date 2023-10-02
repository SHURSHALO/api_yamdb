from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet, UserCreateViewSet, UserGetTokenViewSet, UserViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'titles', TitleViewSet),
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'users', UserViewSet, basename='users')

auth_router_v1 = SimpleRouter()
auth_router_v1.register(r'signup', UserCreateViewSet, basename='signup')
auth_router_v1.register(r'token', UserGetTokenViewSet, basename='token')

urlpatterns = [
    path('v1/auth/', include(auth_router_v1.urls)),
    path('v1/', include(router_v1.urls)),
]
