
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Review, Comment
from api.serializers import ReviewSerializer, CommentSerializer
from rest_framework import permissions
from api.permissions import AuthorOrReadOnly, ReadOnly, IsAdminOrModeratorOrAuthor
from rest_framework import viewsets, pagination, mixins, filters
from django.shortcuts import get_object_or_404

from .permissions import IsAdminOrReadOnly
from django.core.mail import EmailMessage
from reviews.models import Title, Genre, Category
from .permissions import IsAdminOrReadOnly
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, mixins, pagination, permissions, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Title
from users.models import User
from .permissions import (IsSuperUserOrAdmin, IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CreateUserSerializer,
                          GenreSerializer, JWTTokenCreateSerializer,
                          TitleSerializer, UserSerializer)
from .utils import send_confirmation_code
from .filters import TitleFilter


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
        return [IsAdminOrModeratorOrAuthor()]

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
        return [IsAdminOrModeratorOrAuthor()]

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
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Представление для создания пользователя."""
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, created = User.objects.get_or_create(
                **serializer.validated_data
            )
            send_confirmation_code(
                user.email,
                default_token_generator.make_token(user),
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class UserGetTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Представление  для создания JWT-токена и"""
    """Представление для создания JWT-токена и отправки кода для его получения."""

    queryset = User.objects.all()
    serializer_class = JWTTokenCreateSerializer
    permission_classes = (permissions.AllowAny,)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get('confirmation_code')
        
        try:
            user = get_object_or_404(User, username=username)
        except User.DoesNotExist:
            message = {"Пользователь не найден."}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        if default_token_generator.check_token(user, confirmation_code):
            message = {"Ваш token -": str(AccessToken.for_user(user))}
            return Response(message, status=status.HTTP_200_OK)
        message = {"Неправильный код подтверждения."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Представление  для управления пользователями."""
    """Представление для управления пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = (IsSuperUserOrAdmin,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["=username"]
    lookup_field = "username"
    @action(
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
        methods=["get", "patch"],
    )
    def me(self, request):
        """Получение данных о пользователе."""
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "GET":
            return Response(serializer.data, status=status.HTTP_200_OK)
        try:
            serializer.validated_data["role"] = request.user.role
            serializer.save()
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)
