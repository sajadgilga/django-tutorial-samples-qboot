from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, BasePermission

from users.models import Book, Comment
from users.serializers import BookSerializer, CommentSerializer


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.id


class BookCrudView(RetrieveUpdateDestroyAPIView):
    """
    CRUD actions for Book model (text, name, author, owner)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    lookup_url_kwarg = 'book_id'


class CommentsView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['book']
    search_fields = ['text']
