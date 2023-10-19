from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, BasePermission

from users.models import Book
from users.serializers import BookSerializer


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
