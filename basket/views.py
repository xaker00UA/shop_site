import json
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseNotFound, JsonResponse
from django.views import View
from .servise import Crud_Basket


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        basket = Crud_Basket.get_basket(request)
        total_price = basket.total_price()
        total_quantity = basket.total_quantity()
        items = []
        for item in basket:
            items.append(
                {
                    "id": item.id,
                    "name": item.product.name,
                    "quantity": item.quantity,
                    "price": item.product_price(),
                }
            )
        data = {
            "status": "success",
            "total_price": total_price,
            "total_quantity": total_quantity,
            "items": items,
        }
        return render(request, "basket/basket.html", {"basket": data})

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            product_id = data.get("product_id")
            res = Crud_Basket.add_to_basket(request.user, product_id=product_id)
            return JsonResponse(res)
        except:
            return JsonResponse({"status": "error"})

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        res = Crud_Basket.update_basket(data)
        return JsonResponse(res)
