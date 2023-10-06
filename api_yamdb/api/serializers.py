from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Genre, Title, Comment, Review
from users.models import User
from reviews.utils import check_year_availability
from api.validators import validate_email, validate_me, validate_username


class ReviewSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Review.'''

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.HiddenField(default=None)

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message='Ваш отзыв уже имеется.',
            )
        ]

    def update(self, instance, validated_data):
        if self.context['request'].method == 'PUT':
            raise exceptions.MethodNotAllowed('PUT method is not allowed')
        return super().update(instance, validated_data)

    def validate(self, data):
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')

        if Review.objects.filter(author=user, title=title_id).exists():
            if self.context['request'].method == 'POST':
                raise ValidationError(
                    {'detail': 'Отзыв для этого title уже существует.'}
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Comment.'''

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.HiddenField(default=None)

    class Meta:
        fields = ('id', 'review', 'text', 'author', 'pub_date')
        model = Comment

    def update(self, instance, validated_data):
        if self.context['request'].method == 'PUT':
            raise exceptions.MethodNotAllowed('PUT method is not allowed')
        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(source='average_rating', read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['genre'] = GenreSerializer(
            instance.genre.all(), many=True
        ).data
        representation['category'] = CategorySerializer(instance.category).data
        return representation

    def validate(self, attrs):
        year = attrs.get('year')
        check_year_availability(year)
        return attrs


class CreateUserSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания User.'''

    email = serializers.EmailField(
        max_length=254,
        required=True,
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )
        validators = [
            validate_me,
            validate_email,
            validate_username,
        ]


class JWTTokenCreateSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания jwt токена.'''

    username = serializers.CharField(
        required=True,
    )
    confirmation_code = serializers.CharField(
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )


class UserSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания пользователя.'''

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    validators = [
        validate_me,
    ]
