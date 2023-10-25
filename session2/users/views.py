from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import Book, Comment, Token
from users.serializers import BookSerializer, CommentSerializer, BookLeanSerializer, UserSerializer

User = get_user_model()


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.id


class BookListView(APIView):
    def get(self, request, pk=None):
        if not pk:
            books = Book.objects.all()
            return Response(BookLeanSerializer(books, many=True).data)
        return Response(BookSerializer(get_object_or_404(Book.objects.all(), pk=pk)).data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        return Response({"message": "success", "data": serializer.data})

    def put(self, request, pk):
        book = get_object_or_404(Book.objects.all(), pk=pk)
        serializer = BookSerializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response({'message': 'success', 'data': serializer.data})

    def patch(self, request, pk):
        book = get_object_or_404(Book.objects.all(), pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response({'message': 'success', 'data': serializer.data})


class BookCrudView(RetrieveUpdateDestroyAPIView):
    """
    CRUD actions for Book model (text, name, author, owner)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    lookup_url_kwarg = 'book_id'


class CommentsView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    # filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_fields = ['book']
    # search_fields = ['text']


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, url_path="comment", url_name="post_comment", permission_classes=[])
    def submit_comment(self, request, pk):
        book = self.get_object()
        comment = Comment.objects.create(text=request.data.get('text', 'default text'), book=book)
        return Response(CommentSerializer(comment).data)

    @submit_comment.mapping.delete
    def delete_comment(self, request, pk):
        comment = Comment.objects.get(pk=self.kwargs.get('pk'))
        comment.delete()
        return Response({"message": "successfully deleted"})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        return Response(UserSerializer(user, context={
            'request': request,
        }).data)


class LoginView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        data = request.data
        user = User.objects.get(username=data.get('username'))
        if not user.check_password(data.get('password')):
            return Response({'message': 'wrong credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        token = Token.get_or_generate_token(user=user)
        return Response({'message': 'success', 'data': {'token': token.code}})
