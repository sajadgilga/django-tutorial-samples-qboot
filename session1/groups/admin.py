from django.contrib import admin, messages

from groups.models import Book


# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'is_open',)
    actions = ('open_book',)

    def open_book(self, request, queryset):
        for item in queryset:
            item.open(request.user)
