from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import СategoriesViewSet, GenresViewSet, CommentsViewSet, TitlesViewSet, ReviewsViewSet

router = DefaultRouter()

#   CATEGORIES
router.register('categories', СategoriesViewSet, basename='categories')
router.register(r'categories/(?P<slug>[-\w]+)/', СategoriesViewSet, basename='categories-slug')

#   GENRES
router.register('genres', GenresViewSet, basename='genres')
router.register(r'genres/(?P<slug>[-\w]+)/', GenresViewSet, basename='genres-slug')

#   TITLES
router.register('titles', TitlesViewSet, basename='titles')
router.register(
    r'titles/(?P<titles_id>\d+)/', TitlesViewSet, basename='titles-pk'
)   # если {titles_id} не является числом то r'titles/(?P<titles_id>[-\w]+)/'  
    # Это выражение позволит извлекать строковые значения titles_id, которые могут содержать буквы, цифры и дефисы.

#   REVIEWS
router.register(
    r'titles/(?P<titles_id>\d+)/reviews/', ReviewsViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/', ReviewsViewSet, basename='reviews-pk'
)

#   COMMENTS
router.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments/', CommentsViewSet, basename='comments'
)
router.register(
    r'titles/(?P<titles_id>\d+)/reviews/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)/', CommentsViewSet, basename='comments-pk'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
