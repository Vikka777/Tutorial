from django import forms
from django.contrib.auth.forms import UserCreationForm, User
from .models import Author, Quote

class UserRegistrationForm(UserCreationForm):
    model = User
    fields = ['username', 'password']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'author']
