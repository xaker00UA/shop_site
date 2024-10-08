from django.urls import path, re_path
from .views import *
from django.views import View

app_name = "catalog"
urlpatterns = [
    path("", CatalogPageView.as_view(), name="catalog"),
    path("add", CreateProduct.as_view(), name="add_product"),
    path("product/<int:product_id>/", ProductPageView.as_view(), name="product"),
    path(
        "product/<int:product_id>/update",
        ProductUpdate.as_view(),
        name="product_update",
    ),
    path(
        "product/<int:product_id>/delete",
        ProductDelete.as_view(),
        name="product_delete",
    ),
]
