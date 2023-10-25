from django.contrib import admin

# Register your models here.
from users.models import Book, Token


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'user')
