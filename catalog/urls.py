from django.urls import path
from .views import HomePageView, CreateProduct, BasketView
from django.views import View


urlpatterns = [
    path("", HomePageView.as_view(), name="catalog"),
    path("add", CreateProduct.as_view(), name="add"),
    path("basket", BasketView.as_view(), name="basket"),
]
