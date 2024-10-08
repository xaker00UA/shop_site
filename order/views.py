import json
from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DeleteView, CreateView, DetailView, ListView
from django.http import (
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
    HttpResponse,
    JsonResponse,
    HttpResponseRedirect,
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CreateOrderForm
from .models import Order, OrderItem
from .servise import CrudOrder
from django.db.models import Prefetch

__all__ = ["Detail_order", "OrderView"]


@method_decorator(login_required, name="dispatch")
class OrderView(View):
    http_method_names = ["post", "delete", "get"]
    model = Order
    template_name = "order/order.html"

    def post(self, request, *args, **kwargs):
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            order = CrudOrder.create_order(data=form.cleaned_data, user=request.user)
            return redirect("order:order_info")

    def get(self, request, *args, **kwargs):
        initial = {
            "name": request.user.name,
            "phone": request.user.phone_number,
            "surname": request.user.surname,
        }
        form = CreateOrderForm(initial)
        return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name="dispatch")
class Detail_order(ListView):
    http_method_names = ["get", "delete"]
    model = Order
    template_name = "order/detail_order.html"
    context_object_name = "orders"

    def get_queryset(self) -> QuerySet[Any]:
        return Order.objects.filter(user=self.request.user).prefetch_related(
            Prefetch("orderitem_set", queryset=OrderItem.objects.all())
        )

    def delete(self, request, *args, **kwargs):
        _id = json.loads(request.body).get("order_id")
        try:
            order = Order.objects.get(id=_id)
            if order.user == request.user:
                order.delete()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"error": "Forbidden"}, status=403)
        except Order.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)
