from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=250, unique=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, unique=True)

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password) -> bool:
        return check_password(password, self.password)

    def save(self, *args, **kwargs):
        if not self.pk:
            # Хешируем пароль только при создании пользователя
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"name={self.name}, email={self.email}, password={self.password}"

    def __repr__(self) -> str:
        fields = ", ".join(
            f"{key}={value!r}"
            for key, value in self.__dict__.items()
            if not key.startswith("_")
        )
        return f"{self.__class__.__name__}({fields})"
