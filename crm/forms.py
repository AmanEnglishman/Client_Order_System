from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Client, Order, Interaction


class UserRegistrationForm(UserCreationForm):
    """Registration form for new users."""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ClientForm(forms.ModelForm):
    """ModelForm for creating and editing clients."""

    class Meta:
        model = Client
        fields = ['name', 'phone', 'secondary_phone', 'email', 'address', 'tags', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'secondary_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: ключевой, VIP'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class InteractionForm(forms.ModelForm):
    """Form for adding client interactions."""

    class Meta:
        model = Interaction
        fields = ['contact_type', 'note']
        widgets = {
            'contact_type': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class OrderForm(forms.ModelForm):
    """ModelForm for creating and editing orders."""

    class Meta:
        model = Order
        fields = ['client', 'total_price', 'status']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
