from django.contrib import admin

# Register your models here.
from users.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
