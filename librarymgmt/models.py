from django.db import models

from core.models import SchoolScopedModel
from students.models import Student


class Library(SchoolScopedModel):
    name = models.CharField(max_length=120)


class Author(SchoolScopedModel):
    name = models.CharField(max_length=120)


class Genre(SchoolScopedModel):
    name = models.CharField(max_length=120)


class Book(SchoolScopedModel):
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=40, blank=True)
    author = models.ForeignKey(Author, null=True, blank=True, on_delete=models.SET_NULL)
    genre = models.ForeignKey(Genre, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=1)


class BookIssue(SchoolScopedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
