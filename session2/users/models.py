import binascii
import os
from datetime import timedelta, datetime

from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.


class Book(models.Model):
    text = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=64)
    author = models.CharField(max_length=128, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, related_name='books')


class Comment(models.Model):
    text = models.TextField()
    book = models.ForeignKey("Book", on_delete=models.CASCADE)


class Token(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    expiration_time = models.DateTimeField()
    code = models.CharField(max_length=128)

    @staticmethod
    def get_or_generate_token(user, expiration_eta=10):
        token = Token.objects.filter(user=user).first()
        if token and token.expiration_time < datetime.now():
            token.delete()
            token = None
        if not token:
            expiration_time = datetime.now() + timedelta(hours=expiration_eta)
            token = Token.objects.create(user=user, expiration_time=expiration_time,
                                         code=binascii.hexlify(os.urandom(20)).decode())
        return token
