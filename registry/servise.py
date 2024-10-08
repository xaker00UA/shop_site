from .models import User
from .models import models
from .form import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from basket.models import Basket


class CrudUser:
    @staticmethod
    def create_user(name, password1, password2, email, salesman):
        if password1 != password2:
            return "Passwords do not match"
        if User.objects.filter(email=email).exists():
            return "Email already exists"
        user = User.objects.create_user(
            name=name, password=password1, email=email, role=salesman
        )
        return True

    @staticmethod
    def get_user(request, email, password1, **kwargs):
        session_key = request.session.session_key
        user = authenticate(request, email=email, password=password1)
        if user is None:
            return False
        else:
            login(request, user)
            Basket.logged(session_key=session_key, user=user)
            return True

    @staticmethod
    def logout_user(request):
        user = request.user
        logout(request)
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        Basket.logout(session_key=session_key, user=user)
        return True

    @staticmethod
    def delete_user(request):
        email = request.user.email
        CrudUser.logout_user(request)
        User.objects.filter(email=email).delete()
        return True

    @staticmethod
    def update_user(
        request,
        new_email,
        old_password,
        new_password,
        repeat_password,
        salesman,
        phone_number,
        telegram_account,
        name,
        **kwargs,
    ):
        user = User.objects.get(email=request.user.email)
        if user:
            if old_password:
                if check_password(old_password, user.password):
                    if new_password == repeat_password:
                        user.password = make_password(new_password)
                        # login(request, user)
                        return True
                    else:
                        return "Passwords do not match"
                else:
                    return "Incorrect old password"
            else:
                user.role = salesman if salesman is not None else user.role
                user.email = new_email if new_email else user.email
                user.name = name if name else user.name
                user.phone_number = phone_number if phone_number else user.phone_number
                user.telegram_account = (
                    telegram_account if telegram_account else telegram_account
                )
            user.save()
            return True
        else:
            return "Incorrect email"
