
from rest_framework import serializers
from reviews.models import Comment, Review
import datetime
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from reviews.models import Title, Category, Genre

from rest_framework.exceptions import ValidationError

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
    
    def validate(self, data):
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')

        if Review.objects.filter(author=user, title=title_id).exists():
            if self.context['request'].method == 'POST':
                raise ValidationError({'detail': 'Отзыв для этого title уже существует.'})
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
