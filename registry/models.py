from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=250, unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=250)
    role = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    phone_number = models.CharField(max_length=15, null=True, blank=True)
    telegram_account = models.CharField(max_length=100, null=True, blank=True)

    objects = CustomUserManager()

    class Meta:
        db_table = "user"

    USERNAME_FIELD = "email"

    def __str__(self):
        return f"name={self.name}, email={self.email}, password={self.password}"

    def __repr__(self) -> str:
        fields = ", ".join(
            f"{key}={value!r}"
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        )
        return f"{self.__class__.__name__}({fields})"
