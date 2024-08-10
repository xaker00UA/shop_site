from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.AuthView.as_view(), name="auth"),
]
