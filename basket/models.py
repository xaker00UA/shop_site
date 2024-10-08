from django.db import models

from catalog.models import Product
from registry.models import User


class BasketQuerySet(models.QuerySet):
    def total_price(self):
        return sum(product.product_price() for product in self)

    def total_quantity(self):
        if self:
            return sum(basket.quantity for basket in self)
        return 0


class Basket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Количество товаров
    date_added = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=32, blank=True, null=True)

    objects = BasketQuerySet.as_manager()

    def product_price(self):
        return round(self.product.price * self.quantity, 2)

    def update_quantity(self, new_quantity=1):
        if new_quantity > 0:
            self.quantity = new_quantity
            self.save()
        else:
            self.delete()

    def set_quantity(self, new_quantity):
        if new_quantity > 0:
            self.quantity = new_quantity
        else:
            self.delete()

    @classmethod
    def logged(cls, session_key, user):
        cls.objects.filter(session_key=session_key).update(user=user, session_key=None)

    @classmethod
    def logout(cls, session_key, user):
        cls.objects.filter(user=user).update(session_key=session_key, user=None)

    def __str__(self):
        return f"{self.product}"

    class Meta:
        db_table = "basket"
        verbose_name = "Basket"
        verbose_name_plural = "Baskets"
        unique_together = ("user", "product")
