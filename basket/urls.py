from django.urls import path
from . import views

app_name = "basket"
urlpatterns = [
    path("", view=views.HomePageView.as_view(), name="basket"),
    path("add/", view=views.HomePageView.as_view(), name="add_basket"),
]
