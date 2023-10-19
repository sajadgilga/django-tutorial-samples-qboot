from django.urls import path

from users.views import BookCrudView

urlpatterns = [
    path('books/', BookCrudView.as_view()),
    path('books/<int:book_id>', BookCrudView.as_view()),
]