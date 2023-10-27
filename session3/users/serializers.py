import requests
from django.contrib.auth.models import User
from rest_framework import serializers


def fetch_from_data_source(text):
    print('fetch from data source called')
    return requests.get("https://example.com")


def text_words_count(text):
    if type(text) == str:
        return fetch_from_data_source(text)
    raise ValueError("text value is not right")


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    name_words = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "full_name", "username", "email", "name_words")

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
