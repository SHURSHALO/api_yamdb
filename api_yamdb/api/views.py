
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Review, Comment
from api.serializers import ReviewSerializer, CommentSerializer
from rest_framework import permissions
from api.permission import OnlyAuthorHasPerm, ReadOnly, ModeratorPermission


class ReviewsViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action == 'retrieve':
            return (permissions.IsAuthenticatedOrReadOnly())
        elif self.request.user.is_authenticated:
            return (ModeratorPermission(),)
        return (OnlyAuthorHasPerm(),)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        if self.action == 'retrieve':
            return (permissions.IsAuthenticatedOrReadOnly())
        return (OnlyAuthorHasPerm(),)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
