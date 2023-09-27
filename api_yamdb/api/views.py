
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Review, Comment
from api.serializers import ReviewSerializer, CommentSerializer
from rest_framework import permissions
from api_yamdb.api.permissions import OnlyAuthorHasPerm, ReadOnly, ModeratorPermission
from rest_framework import viewsets, pagination, mixins, filters

from reviews.models import Title, Genre, Category
from .permissions import IsAdminOrReadOnly
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer


class ReviewsViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action == 'retrieve':
            return (permissions.IsAuthenticatedOrReadOnly())
        elif self.request.user.is_authenticated:
            return (ModeratorPermission(),)
        return (OnlyAuthorHasPerm(),)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action == 'retrieve':
            return (permissions.IsAuthenticatedOrReadOnly())
        return (OnlyAuthorHasPerm(),)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CreateListDestroyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = pagination.LimitOffsetPagination  # Или глобально
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category', 'genre', 'name', 'year')
    # permission_classes = IsAdminOrReadOnly


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    # permission_classes = IsAdminOrReadOnly


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    # permission_classes = IsAdminOrReadOnly
