
from rest_framework import serializers
from reviews.models import Comment, Review


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
