from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import CategoryViewSet, GenreViewSet, CommentsViewSet, TitleViewSet, ReviewsViewSet

from .views import TitleViewSet, GenreViewSet, UsersViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet, UserCreateViewSet, UserGetTokenViewSet, UserViewSet)

from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet, UserCreateViewSet, UserGetTokenViewSet, UserViewSet)

from rest_framework.routers import DefaultRouter
from api.views import CategoryViewSet, GenreViewSet, CommentsViewSet, TitleViewSet, ReviewsViewSet


router_v1 = DefaultRouter()

router_v1.register(r'titles', TitleViewSet),
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'users', UserViewSet, basename='users')

auth_router_v1 = SimpleRouter()
auth_router_v1.register(r'signup', UserCreateViewSet, basename='signup')
auth_router_v1.register(r'token', UserGetTokenViewSet, basename='token')


#   REVIEWS
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewsViewSet, basename='reviews')


#   COMMENTS
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentsViewSet, basename='comments'
)


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('v1/auth/', include(auth_router_v1.urls)),
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
