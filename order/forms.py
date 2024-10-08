from django import forms
from .models import Order


class CreateOrderForm(forms.Form):

    name = forms.CharField(max_length=50)

    surname = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=20)
    address = forms.CharField(max_length=100)
