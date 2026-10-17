from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "status", "rating"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5, "placeholder": "1-5 (optional)"}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is not None and not 1 <= rating <= 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating
