
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Review, Comment
from api.serializers import ReviewSerializer, CommentSerializer
from rest_framework import permissions
from api.permissions import AuthorOrReadOnly, ReadOnly, ModeratorOrAuthPermission
from rest_framework import viewsets, pagination, mixins, filters
from django.shortcuts import get_object_or_404
from reviews.models import Title, Genre, Category
from .permissions import IsAdminOrReadOnly
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer


class ReviewsViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        elif self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [ModeratorOrAuthPermission()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentsViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_reviews(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_reviews().comments.all()

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        elif self.action == 'retrieve':
            return [permissions.AllowAny()]
        return [ModeratorOrAuthPermission()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_reviews())


# def get_permissions(self):
#         if self.action == 'list':
#             return (permissions.AllowAny())
#         elif self.action == 'retrieve':
#             return (permissions.AllowAny())
#         elif self.action == 'create':
#             return (ModeratorOrAuthPermission(),)
#         elif self.action == 'update' or self.action == 'partial_update':
#             return (ModeratorOrAuthPermission(),)  # Например, своя кастомная проверка
#         elif self.action == 'destroy':
#             return (ModeratorOrAuthPermission(),)  # Ещё одна кастомная проверка
#         return super().get_permissions()




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
