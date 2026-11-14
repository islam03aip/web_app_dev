from django.contrib import admin

from .models import Author, Book, Category, Review

admin.site.register([Author, Book, Category, Review])
