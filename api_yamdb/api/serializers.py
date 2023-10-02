import datetime

from rest_framework import serializers
from reviews.models import Category, Genre, Title
from users.models import User

from .validators import validate_email, validate_me, validate_username


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(many=True, slug_field='slug',
                                         queryset=Genre.objects.all())
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = '__all__'

    def validate(self, attrs):
        year = attrs.get('year')
        current_year = datetime.datetime.now().year
        if year and year >= current_year:
            raise serializers.ValidationError(
                "Год должен быть меньше текущего года.")
        return attrs


class CreateUserSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания User. """

    email = serializers.EmailField(max_length=254, required=True,)
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$", max_length=150, required=True,
    )

    class Meta:
        model=User
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
    """ Сериализатор для создания jwt токена. """

    username = serializers.CharField(required=True,)
    confirmation_code = serializers.CharField(required=True,)

    class Meta:
        model=User
        fields = (
            "username",
            "confirmation_code",
        )


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания пользователя. """

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )

    validators = [
        validate_me,
    ]
