from django.contrib import admin

from .models import Author, Book, BookIssue, Genre, Library

admin.site.register(Library)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(BookIssue)
