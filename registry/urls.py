from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    path("", view=views.LoginUser.as_view(), name="login"),
    path("registry", view=views.RegisterUser.as_view(), name="register_user"),
    path("logout", view=views.LoginUser.as_view(), name="logout"),
    path("profile", view=views.UserProfile.as_view(), name="profile"),
    path("update", view=views.UserProfile.as_view(), name="user_update"),
]
