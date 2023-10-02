
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
from reviews.models import Title, Genre, Category, User
from .permissions import IsAdminOrReadOnly
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer, UserSerializer, NotAdminSerializer, SignUpSerializer, GetTokenSerializer
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
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Title
from users.models import User

from .permissions import (IsAdminOrModeratorOrAuthor, IsSuperUserOrAdmin,
                          ReadOnly)
from .serializers import (CategorySerializer, CreateUserSerializer,
                          GenreSerializer, JWTTokenCreateSerializer,
                          TitleSerializer, UserSerializer)
from .utils import send_confirmation_code


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


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, AdminOnly,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)
    

class APIGetToken(APIView):
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Доброе время суток, {user.username}.'
            f'\nКод подтвержения для доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтвержения для доступа к API!'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
