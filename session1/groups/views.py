import json
from http import HTTPStatus

from django.contrib.auth.models import User
from django.http import JsonResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from groups.models import Book


class BookEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Book):
            result = obj.__dict__.copy()
            result.pop('_state')
            result['owner'] = obj.owner
            return result
        elif isinstance(obj, User):
            result = {'username': obj.username, 'id': obj.id}
            return result
        return super().default(obj)


def book_encoder(obj):
    result = obj.__dict__
    result.pop('_state')
    result.pop('author')
    result.pop('is_open')
    result['owner'] = obj.owner
    return result


# method view implementation
def retrieve_book(request, book_id=1):
    try:
        book = Book.objects.get(id=book_id)
        return JsonResponse(book, safe=False, encoder=BookEncoder)
    except Book.DoesNotExist:
        return JsonResponse({'message': 'Book not found'}, status=HTTPStatus.NOT_FOUND)


# class view implementation
@method_decorator(csrf_exempt, name='dispatch')
class RetrieveCreateBookView(View):
    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            print(f'in get method handler {book.id}')
            return JsonResponse(book, safe=False, encoder=BookEncoder)
        except Book.DoesNotExist:
            return JsonResponse({'message': 'Book not found'}, status=HTTPStatus.NOT_FOUND)

    def post(self, request: HttpRequest):
        data = json.loads(request.body.decode('utf-8'))
        print('name: ', request.POST.get('name'))
        book = Book.objects.create(name=data['name'], author=data['author'], is_open=False,
                                   content=data['content'])
        return JsonResponse({'message': 'Book was created successfully'})


# Get book list view
class RetrieveBookListView(View):
    def get(self, request):
        books = Book.objects.all()[:10]
        return JsonResponse(list(books), safe=False, encoder=BookEncoder)
