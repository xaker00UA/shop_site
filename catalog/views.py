from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from . import servise
from django.views import View
from .form import ProductForm
from django.utils.decorators import method_decorator


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        print(request)
        prod = servise.get_product()
        return render(request, "catalog/home.html", context={"product": prod})

    # @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        print(request)
        print(request.POST.get("product_id"))
        print(request.user)
        servise.add_to_basket(request.POST.get("product_id"), request.user)
        return redirect("basket")


@method_decorator(login_required, name="dispatch")
class CreateProduct(View):
    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("catalog")
        return render(request, "catalog/upload.html", {"form": ProductForm()})

    def get(self, request, *args, **kwargs):
        return render(request, "catalog/upload.html", {"form": ProductForm()})


@method_decorator(login_required, name="dispatch")
class BasketView(View):
    def get(self, request, *args, **kwargs):
        data = servise.get_basket(request.user.id)
        return render(request, "catalog/basket.html", context={"basket": data})

    def delete(self, request, *args, **kwargs):
        pass
