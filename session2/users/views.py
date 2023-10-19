import json

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Book
from users.serializers import BookSerializer


class BookEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Book):
            return {"id": o.id, "name": o.name, 'text': o.text, "author": o.author, "owner": o.owner_id}
        return super().default(o)


class BookCrudView(APIView):
    """
    CRUD actions for Book model (text, name, author, owner)
    """
    permission_classes = [IsAuthenticated]

    def get_book_by_id(self, pk):
        try:
            book = Book.objects.get(pk=pk)
            return book
        except Book.DoesNotExist:
            return None

    def check_authentication(self, request):
        if not request.user.is_authenticated:
            return False
        return True

    def is_owner(self, book, user):
        return user.id == book.owner_id

    def validate_book(self, data):
        errors = {}

        def check_required_field(field, errors):
            if field not in data or not data[field]:
                errors[field] = 'This field is required'
                return False
            return data[field]

        name = check_required_field('name', errors)
        author = check_required_field('author', errors)
        text = check_required_field('text', errors)

        if name:
            if len(name) < 3:
                errors['name'] = 'name field should be more than 3 chars'

        return errors

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('pk')
        if book_id:
            book = self.get_book_by_id(book_id)
            if book:
                return Response(BookSerializer(book).data)
            return Response({"error": "Book not found"}, status=404)

        books = Book.objects.all()
        return Response(BookSerializer(books, many=True).data)

    def post(self, request, *args, **kwargs):
        if not self.check_authentication(request):
            return Response({"error": "Authentication required"}, status=401)

        data = json.loads(request.body)
        errors = self.validate_book(data)
        if errors:
            return Response(errors, safe=False, status=400)

        book = Book.objects.create(name=data.get('name'), text=data.get('text'), author=data.get('author'),
                                   owner=request.user)
        return Response({"message": "Book created", "data": book}, encoder=BookEncoder)

    def run_checks_and_get_object(self, request, pk):
        if not self.check_authentication(request):
            return Response({"error": "Authentication required"}, status=401)

        book = self.get_book_by_id(pk)
        if not book:
            return Response({"error": "Book not found"}, status=404)

        if not self.is_owner(book, request.user):
            return Response({"error": "Not authorized for this action"}, status=403)
        return book

    def put(self, request, pk, *args, **kwargs):
        result = self.run_checks_and_get_object(request, pk)
        if not isinstance(result, Book):
            return result
        book = result

        data = json.loads(request.body)
        errors = self.validate_book(data)
        if errors:
            return Response(errors, status=400)

        book.text = data.get('text')
        book.name = data.get('name')
        book.author = data.get('author')
        book.save()
        return Response({"message": "Book updated"})

    def patch(self, request, pk, *args, **kwargs):
        result = self.run_checks_and_get_object(request, pk)
        if not isinstance(result, Book):
            return result
        book = result

        data = json.loads(request.body)

        if 'name' in data:
            book.name = data.get('name')
        if 'text' in data:
            book.text = data.get('text')
        if 'author' in data:
            book.author = data.get('author')
        book.save()
        return Response({"message": "Book partially updated"})

    def delete(self, request, pk, *args, **kwargs):
        result = self.run_checks_and_get_object(request, pk)
        if not isinstance(result, Book):
            return result
        book = result

        book.delete()
        return Response({"message": "Book deleted"}, status=201)
