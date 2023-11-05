# Create your views here.
import datetime

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Comment, ImageUpload, GlobalConfig
from users.serializers import UserSerializer, RegisterSerializer, CommentSerializer, ImageUploadSerializer
from users.tasks import generate_thumbnail

User = get_user_model()

PROFILE_CACHE_KEY = 'user_profile_'


class RegisterApiView(CreateAPIView):
    serializer_class = RegisterSerializer


class ProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # r = chain(addition.s(3, 2) | custom_formula.s())()
        # print('result is', r.get())
        return self.get_queryset().get(pk=self.request.user.id)


class CommentListView(ListAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(name=self.request.query_params.get('query'))


async def get_profile(request, pk, *args, **kwargs):
    users = User.objects.filter(pk=pk)
    user = users.aget(pk=pk)
    async for user in User.objects.filter():
        print('user is:', user.username)
    return HttpResponse(f'"username": "{user.username}","id": "{user.id}"')


def comment_page(request):
    comments = Comment.objects.all()[:10]
    return render(request, 'comments.html', {'comments': comments})


@api_view(['GET'])
def steal_data(request):
    print(request.GET.get('token'))
    return Response()


class ImageUploadView(CreateAPIView):
    serializer_class = ImageUploadSerializer
    queryset = ImageUpload.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        config = GlobalConfig.load()
        if config.start_time < datetime.datetime.now() < config.end_time:
            generate_thumbnail.delay(instance.id)
