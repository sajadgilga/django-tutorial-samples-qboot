from django.urls import path

from users.routers import CustomRouter
from users.views import CommentsView, BookViewSet, BookListView, ProfileView, LoginView

router = CustomRouter()
router.register('book_set', BookViewSet)

urlpatterns = [
                  path('profile', ProfileView.as_view(), name='user-profile'),
                  path('auth/login', LoginView.as_view()),
                  path('books/', BookListView.as_view()),
                  path('books/<int:pk>', BookListView.as_view()),
                  # path('book_set/<int:pk>', BookViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
                  # path('book_set/', BookViewSet.as_view({'get': 'list', 'post': 'create'})),
                  path('books/comments', CommentsView.as_view()),
              ] + router.urls
