import datetime

from rest_framework import serializers

from reviews.models import Title, Category, Genre


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
