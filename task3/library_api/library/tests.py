from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book, Category


class LibraryAPITests(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Frank Herbert")
        self.cat = Category.objects.create(name="Sci-Fi")
        self.book = Book.objects.create(title="Dune", isbn="9780441013593",
                                        published_year=1965, price="9.99", author=self.author)
        self.book.categories.add(self.cat)

    def test_author_crud(self):
        r = self.client.post("/api/authors/", {"name": "Ursula Le Guin"}, format="json")
        self.assertEqual(r.status_code, 201)
        aid = r.data["id"]
        self.assertEqual(self.client.get(f"/api/authors/{aid}/").status_code, 200)
        self.assertEqual(self.client.put(f"/api/authors/{aid}/", {"name": "UKLG", "bio": "x"}, format="json").status_code, 200)
        self.assertEqual(self.client.patch(f"/api/authors/{aid}/", {"bio": "y"}, format="json").status_code, 200)
        self.assertEqual(self.client.delete(f"/api/authors/{aid}/").status_code, 204)
        self.assertEqual(self.client.get(f"/api/authors/{aid}/").status_code, 404)

    def test_author_books(self):
        r = self.client.get(f"/api/authors/{self.author.id}/books/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.data), 1)

    def test_book_validation(self):
        bad = {"title": "X", "isbn": "123", "published_year": 3000, "price": "-1", "author": self.author.id}
        r = self.client.post("/api/books/", bad, format="json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual(set(r.data), {"isbn", "published_year", "price"})

    def test_book_missing_author(self):
        r = self.client.post("/api/books/", {"title": "X", "isbn": "1234567890123",
                             "published_year": 2000, "price": "5", "author": 999}, format="json")
        self.assertEqual(r.status_code, 400)

    def test_book_filters(self):
        self.assertEqual(len(self.client.get(f"/api/books/?category={self.cat.id}").data), 1)
        self.assertEqual(len(self.client.get("/api/books/?search=zzz").data), 0)

    def test_reviews(self):
        url = f"/api/books/{self.book.id}/reviews/"
        r = self.client.post(url, {"reviewer_name": "Ann", "rating": 5, "comment": "Great"}, format="json")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(self.client.post(url, {"reviewer_name": "Bob", "rating": 9}, format="json").status_code, 400)
        self.assertEqual(len(self.client.get(url).data), 1)
        self.assertEqual(self.client.get(f"/api/books/{self.book.id}/").data["average_rating"], 5.0)
        rid = r.data["id"]
        self.assertEqual(self.client.patch(f"/api/reviews/{rid}/", {"rating": 4}, format="json").status_code, 200)
        self.assertEqual(self.client.delete(f"/api/reviews/{rid}/").status_code, 204)

    def test_duplicate_category(self):
        r = self.client.post("/api/categories/", {"name": "Sci-Fi"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
