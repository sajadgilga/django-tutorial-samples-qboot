from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.


class Book(models.Model):
    text = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=64)
    author = models.CharField(max_length=128, null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)


class Comment(models.Model):
    text = models.TextField()
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
