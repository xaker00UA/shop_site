from django.db import models
from django.forms import ValidationError


class OrderItemQuerySet(models.QuerySet):
    def total_price(self):
        return sum(item.total_price() for item in self)

    def total_quantity(self):
        if self:
            return sum(item.quantity for item in self)
        return 0


class Order(models.Model):
    user = models.ForeignKey("registry.User", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=True)
    surname = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    phone = models.CharField(max_length=15, verbose_name="телефон")
    address = models.CharField(
        blank=True, null=True, max_length=255, verbose_name="адрес"
    )
    is_paid = models.BooleanField(default=False, verbose_name="Оплата")
    status = models.CharField(
        max_length=20,
        choices=[
            ("delivered", "Delivered"),
            ("completed", "Completed"),
            ("canceled", "Canceled"),
        ],
        default="completed",
    )

    def clean(self):
        # Если пользователь не указан, проверяем обязательность имени и фамилии
        if not self.user:
            if not self.name or not self.surname:
                raise ValidationError(
                    "Имя и фамилия обязательны, если пользователь не указан."
                )

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey("catalog.Product", on_delete=models.SET_NULL, null=True)

    objects = OrderItemQuerySet.as_manager()

    def total_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f"Товар: {self.name} | №Заказ: {self.order.pk}"

    class Meta:
        ordering = ["-created_at"]
        db_table = "order_item"
        verbose_name = "Проданные товары"
