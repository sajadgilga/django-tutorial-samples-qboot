from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class Comment(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, null=True, related_name='comments')
    name = models.CharField(max_length=64, null=True, db_index=True)


class ImageUpload(models.Model):
    original_image = models.ImageField(upload_to='images/')
    thumbnail = models.ImageField(upload_to='images/thumbnails/', null=True, blank=True)


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class GlobalConfig(SingletonModel):
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
