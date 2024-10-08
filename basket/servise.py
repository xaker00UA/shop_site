from .models import Basket
from catalog.models import Product
from django.db import transaction


class Crud_Basket:
    @staticmethod
    def get_basket(request):
        user = request.user
        if user.is_authenticated:
            basket = Basket.objects.filter(user=user)
        else:
            session_key = request.session.session_key
            basket = Basket.objects.filter(session_key=session_key)

        return basket

    @staticmethod
    def add_to_basket(user, product_id):
        product = Product.objects.get(id=product_id)
        basket = Basket.objects.filter(user=user, product=product).first()
        if basket:
            q = basket.quantity
            q += 1
            basket.update_quantity(q)
        else:
            basket = Basket.objects.create(user=user, product=product)
        return {"success": "ok"}

    @staticmethod
    def update_basket(data: dict):
        basket_ids = list(data.keys())

        try:
            with transaction.atomic():
                baskets = Basket.objects.filter(id__in=basket_ids)
                for basket in baskets:
                    quantity = data[str(basket.id)]
                    basket.update_quantity(quantity)
            return {"success": "ok"}
        except Basket.DoesNotExist:
            return {"error": "Basket item not found"}
        except Exception as e:
            return {"error": str(e)}
