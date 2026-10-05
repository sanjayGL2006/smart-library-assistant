from django.contrib import admin
from .models import Category, Author, Book, Student, IssuedBook
for m in (Category, Author, Book, Student, IssuedBook):
    admin.site.register(m)
