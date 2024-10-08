from typing import Any
from .models import User
from django import forms
from django.contrib.auth import authenticate


class UserRegisterForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=100)
    email = forms.EmailField(label="Email", max_length=254)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Assert Password")
    salesman = forms.BooleanField(label="Salesman", initial=False, required=False)


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "name@example.com"}
        ),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
    )


class UserProfileForm(forms.Form):
    name = forms.CharField(
        label="Имя",
        max_length=100,
        required=False,
    )
    new_email = forms.EmailField(label="Email", max_length=254, required=False)
    phone_number = forms.CharField(
        label="Номер телефона", max_length=15, required=False
    )
    telegram_account = forms.CharField(
        label="Телеграм аккаунт", max_length=100, required=False
    )
    salesman = forms.BooleanField(label="Продавец", required=False)
    old_password = forms.CharField(
        widget=forms.PasswordInput, label="Старый пароль", required=False
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput, label="Новый пароль", required=False
    )
    repeat_password = forms.CharField(
        widget=forms.PasswordInput, label="Повтор нового пароля", required=False
    )
