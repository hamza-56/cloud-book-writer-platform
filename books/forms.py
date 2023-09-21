from django import forms
from django.contrib.auth import get_user_model

from .models import Book, Section


User = get_user_model()


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title"]
        labels = {
            "title": "Book Title",
        }


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["title", "text"]
        labels = {
            "title": "Section Title",
            "text": "Section Text",
        }
