from django.urls import path
from .views import *

app_name = "order"

urlpatterns = [
    path("", view=Detail_order.as_view(), name="order_info"),
    path("order", view=OrderView.as_view(), name="order"),
]
