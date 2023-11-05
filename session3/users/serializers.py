import requests
from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Comment, ImageUpload


def fetch_from_data_source(text):
    print('fetch from data source called')
    return requests.get("https://example.com")


def text_words_count(text):
    if type(text) == str:
        return fetch_from_data_source(text)
    raise ValueError("text value is not right")


class CommentLeanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['owner']


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ['original_image', 'id']


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    # comments = CommentLeanSerializer(many=True)

    # name_words = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "full_name", "username", "email")

    def get_full_name(self, user):
        if not user.first_name and not user.last_name:
            return None
        name = ''
        if user.first_name:
            name += f'{user.first_name} '
        if user.last_name:
            name += user.last_name
        return name

    def get_name_words(self, user):
        return text_words_count(f'{user.first_name} {user.last_name} {user.username}')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    def create(self, validated_data):
        user, created = User.objects.get_or_create(username=validated_data.get('username'))
        if not created:
            raise serializers.ValidationError('user already exists in database')
        return user

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError("password & second password do not match")
        return super().validate(attrs)
