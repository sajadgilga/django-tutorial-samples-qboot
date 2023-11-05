from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class BookCategory(models.IntegerChoices):
    novel = 0, 'novel'
    article = 1, 'article'


class Book(models.Model):
    name = models.CharField(max_length=64)
    added_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=False, blank=False)
    category = models.IntegerField(choices=BookCategory.choices)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
