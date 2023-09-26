
from rest_framework import viewsets


from api.models import Сategories, Genres, Reviews, Comments, Titles
from api.serializers import СategoriesSerializer, GenresSerializer, ReviewsSerializer, CommentsSerializer, TitlesSerializer


class СategoriesViewSet(viewsets.ModelViewSet):

    queryset = Сategories.objects.all()
    serializer_class = СategoriesSerializer


class GenresViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class ReviewsViewSet(viewsets.ModelViewSet):

    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer


class TitlesViewSet(viewsets.ModelViewSet):

    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer


class CommentsViewSet(viewsets.ModelViewSet):

    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

