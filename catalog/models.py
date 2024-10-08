from django.db import models

from registry.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "category"

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    description = models.TextField(blank=True, max_length=250)
    image = models.ImageField(blank=True, upload_to="product/", max_length=250)
    image_url = models.URLField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "product"
