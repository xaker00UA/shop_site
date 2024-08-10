from .models import User
from .models import models
from django.contrib.auth.hashers import make_password, check_password


def create_user(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    name = request.POST.get("name")
    user = User.objects.create(email=email, password=password, name=name)
    user.save()
    return user


def update_user(data: dict):
    pass


def delete_user(data: dict):
    pass


def get_user(request):
    try:
        user = User.objects.get(
            name=request.POST.get("name")
        )  # Используйте 'username' вместо 'name'
        if user.check_password(request.POST.get("password")):
            return user  # Если пользователь не найден
    except:
        return None
