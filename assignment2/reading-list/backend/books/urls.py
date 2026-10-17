from django.urls import path

from .pages import BookCreatePage, BookDeletePage, BookListPage, BookUpdatePage

urlpatterns = [
    path("", BookListPage.as_view(), name="home"),
    path("books/add/", BookCreatePage.as_view(), name="book_add"),
    path("books/<int:pk>/edit/", BookUpdatePage.as_view(), name="book_edit"),
    path("books/<int:pk>/delete/", BookDeletePage.as_view(), name="book_delete"),
]
