# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserSerializer

User = get_user_model()

PROFILE_CACHE_KEY = 'user_profile_'


class ProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.get_queryset().get(pk=self.request.user.id)
