from django.contrib import admin

# Register your models here.
from users.models import Comment, ImageUpload, GlobalConfig


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text']


@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(GlobalConfig)
class GlobalConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_time', 'end_time']
