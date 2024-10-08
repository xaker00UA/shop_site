from .models import Order, OrderItem
from basket.models import Basket
from django.db import transaction


class CrudOrder:
    @staticmethod
    def create_order(data, user):
        if user:
            baskets = Basket.objects.filter(user=user)
            order = Order(user=user, **data)
        if not baskets.exists():
            order.delete()
            return {"error": "Корзина пуста."}

        order_items = []
        for basket in baskets:
            order_item = OrderItem(
                order=order,
                product=basket.product,
                price=basket.product_price(),
                quantity=basket.quantity,
                name=basket.product.name,
            )
            order_items.append(order_item)
        order.total_price = baskets.total_price()
        with transaction.atomic():
            order.save()
            OrderItem.objects.bulk_create(order_items)

        baskets.delete()
        return order.id
