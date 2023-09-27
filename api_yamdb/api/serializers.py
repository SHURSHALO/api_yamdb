
from rest_framework import serializers
from reviews.models import Comment, Review
import datetime

from rest_framework import serializers

from reviews.models import Title, Category, Genre


class ReviewSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Review.'''
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Comment.'''
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

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
