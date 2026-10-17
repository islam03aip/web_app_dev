from django.db import connection
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    ordering_fields = ["created_at", "title", "rating"]

    def get_queryset(self):
        qs = Book.objects.all()
        status = self.request.query_params.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs


@api_view(["GET"])
def health(request):
    with connection.cursor() as cur:
        cur.execute("SELECT 1")
    return Response({"status": "ok", "books": Book.objects.count()})
