from django.urls import path

from users.views import BookCrudView

urlpatterns = [
    path('books/', BookCrudView.as_view()),
    path('books/<int:pk>', BookCrudView.as_view()),
]