from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import ProfileView, RegisterApiView, comment_page, CommentListView, steal_data, \
    ImageUploadView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile', ProfileView.as_view(), name='user_profile_info'),
    path('comment-list', CommentListView.as_view(), name='comment_list'),
    path('register', RegisterApiView.as_view(), name='register_user'),
    path('comments', comment_page, name='comment_page'),
    path('steal-data', steal_data, name='steal_data'),
    path('image-upload', ImageUploadView.as_view(), name='image_upload'),
]
