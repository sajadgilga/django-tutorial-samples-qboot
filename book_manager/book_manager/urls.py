from rest_framework.routers import SimpleRouter

from book_manager.views import BookViewSet

router = SimpleRouter()
router.register('books', BookViewSet, basename='book_viewset')

urlpatterns = router.urls
