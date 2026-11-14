import datetime

from rest_framework import serializers

from .models import Author, Book, Category, Review


class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(source="books.count", read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "bio", "birth_date", "book_count", "created_at"]
        read_only_fields = ["created_at"]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be blank.")
        return value.strip()

    def validate_birth_date(self, value):
        if value and value > datetime.date.today():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)
    categories = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), required=False
    )
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ["id", "title", "isbn", "published_year", "price",
                  "author", "author_name", "categories", "average_rating"]

    def get_average_rating(self, obj):
        ratings = list(obj.reviews.values_list("rating", flat=True))
        return round(sum(ratings) / len(ratings), 2) if ratings else None

    def validate_isbn(self, value):
        if not (value.isdigit() and len(value) == 13):
            raise serializers.ValidationError("ISBN must be exactly 13 digits.")
        return value

    def validate_published_year(self, value):
        if value > datetime.date.today().year:
            raise serializers.ValidationError("Published year cannot be in the future.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "book", "reviewer_name", "rating", "comment", "created_at"]
        read_only_fields = ["book", "created_at"]
