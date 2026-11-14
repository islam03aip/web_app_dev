from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Author, Book, Category, Review
from .serializers import (AuthorSerializer, BookSerializer,
                          CategorySerializer, ReviewSerializer)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    @action(detail=True, methods=["get"])
    def books(self, request, pk=None):
        """GET /api/authors/{id}/books/ - all books by this author."""
        author = self.get_object()
        return Response(BookSerializer(author.books.all(), many=True).data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer

    def get_queryset(self):
        qs = Book.objects.select_related("author").prefetch_related("categories", "reviews")
        p = self.request.query_params
        if p.get("author"):
            qs = qs.filter(author_id=p["author"])
        if p.get("category"):
            qs = qs.filter(categories__id=p["category"])
        if p.get("search"):
            qs = qs.filter(title__icontains=p["search"])
        return qs

    @action(detail=True, methods=["get", "post"])
    def reviews(self, request, pk=None):
        """GET/POST /api/books/{id}/reviews/"""
        book = self.get_object()
        if request.method == "GET":
            return Response(ReviewSerializer(book.reviews.all(), many=True).data)
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(book=book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
