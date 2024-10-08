from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
    JsonResponse,
)
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from basket.models import Basket
from .servise import Crud_Product
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from .form import ProductForm
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from .models import Product


__all__ = [
    "CatalogPageView",
    "ProductPageView",
    "ProductUpdate",
    "ProductDelete",
    "CreateProduct",
]


class CatalogPageView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        queryset = Product.objects.select_related("category", "seller")
        price_min = self.request.GET.get("price_min")
        price_max = self.request.GET.get("price_max")
        category = self.request.GET.get("category")
        seller = self.request.GET.get("seller")
        sort = self.request.GET.get("sort")
        if price_min:
            try:
                queryset = queryset.filter(price__gte=int(price_min))
            except ValueError:
                pass
        if price_max:
            try:
                queryset = queryset.filter(price__lte=int(price_max))
            except ValueError:
                pass
        if category and (isinstance(category, (int, float)) or category.isdigit()):
            queryset = queryset.filter(category=int(category))
        if seller and (isinstance(seller, (int, float)) or seller.isdigit()):
            queryset = queryset.filter(seller_id=int(seller))
        sort_options = {
            "cheap": "price",
            "expensive": "-price",
            "name": "name",
            "name_desc": "-name",
            "newest": "-created_at",
        }
        queryset = queryset.order_by(sort_options.get(sort, "price"))

        return queryset


# @method_decorator(login_required, name="dispatch")
class ProductPageView(DetailView):
    model = Product
    template_name = "catalog/product.html"
    context_object_name = "product"
    http_method_names = ["get", "post"]
    pk_url_kwarg = "product_id"

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return super().get_object(queryset)

    def get(self, request, *args, **kwargs):
        product = Crud_Product.read_product(kwargs.get("product_id", -1))
        return render(
            request,
            "catalog/product.html",
            context={
                "product": product,
                "role": (
                    "AnonymousUser"
                    if request.user.is_anonymous != "AnonymousUser"
                    else request.user.role
                ),
            },
        )

    def post(self, request, *args, **kwargs):
        pr = Product.objects.get(id=kwargs.get("product_id"))
        basket = Basket.objects.get(user=request.user, product=pr)
        if basket:
            q = basket.quantity
            q += 1
            basket.update_quantity(q)
        else:
            basket = Basket.objects.create(user=request.user, product=pr)
        return JsonResponse(data={"success": "ok"})


class ProductUpdate(UpdateView):
    model = Product
    template_name = "catalog/update.html"
    pk_url_kwarg = "product_id"
    fields = ["name", "price", "description", "category", "image"]

    def get_success_url(self):
        product = self.object
        return reverse("catalog:product", kwargs={"product_id": product.id})


class ProductDelete(DeleteView):
    model = Product
    pk_url_kwarg = "product_id"
    http_method_names = ("DELETE",)

    def get_success_url(
        self,
    ):

        return "test"
        # return reverse("catalog:product", args="seller=1")
        # return reverse_lazy("catalog:catalog", args=)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        if product.seller != request.user:
            data = {
                "status": "error",
                "error": {
                    "message": "Вы не имеете права удалять этот товар.",
                    "code": 403,
                    "product_id": product.id,
                },
            }
            return JsonResponse(data=data, status=403)

        product.delete()
        data = {
            "status": "success",
            "data": {
                "message": "Товар успешно удалён.",
                "product_id": product.id,
                "success_url": self.get_success_url(),
            },
        }
        return JsonResponse(data=data, status=200)

    # def post(self, request, *args, **kwargs):
    #     # Возвращаем ошибку для POST запросов (если DELETE только разрешен)
    #     data = {
    #         "status": "error",
    #         "error": {
    #             "message": "POST-запросы на этот URL не поддерживаются.",
    #             "code": 405,
    #         },
    #     }
    #     return JsonResponse(
    #         data=data,
    #         status=405,
    #         json_dumps_params={"indent": 4, "ensure_ascii": False},
    #     )

    # def get(self, request, *args, **kwargs):

    #     data = {
    #         "status": "error",
    #         "error": {
    #             "message": "GET-запросы на этот URL не поддерживаются.",
    #             "code": 405,
    #         },
    #     }
    #     return JsonResponse(
    #         data=data,
    #         status=405,
    #         json_dumps_params={"indent": 4, "ensure_ascii": False},
    #     )


@method_decorator(login_required, name="dispatch")
class CreateProduct(CreateView):
    model = Product
    template_name = "catalog/upload.html"
    form_class = ProductForm
    success_url = reverse_lazy("catalog:catalog")

    def form_valid(self, form):
        if self.user_has_seller_role():
            return super().form_valid(form)
        url = reverse("user:profile")
        res = (
            "<html><body>"
            "<h1>Доступ запрещен</h1>"
            '<p>У вас нет роли продавца. Вы можете <a href="{}">посмотреть свой профиль</a> для получения дополнительной информации.</p>'
            "</body></html>"
        ).format(url)
        return HttpResponseForbidden(res)

    def user_has_seller_role(self):
        return self.request.user.role
