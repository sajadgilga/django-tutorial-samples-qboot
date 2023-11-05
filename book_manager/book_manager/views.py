# Create your views here.
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.viewsets import GenericViewSet

from book_manager.serializers import BookSerializer


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.owner_id


class BookViewSet(GenericViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwner]
