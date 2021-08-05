from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'author', 'publication', 'available_quantity')

admin.site.register(Book, BookAdmin)
