from .models import Basket, Category, Product


def get_product():
    return Product.objects.all()


def add_to_basket(product_id, user_id):
    product = Product.objects.get(id=product_id)
    basket, _ = Basket.objects.get_or_create(user=user_id)
    basket.products.add(product)
    basket.save()


def get_category():
    return Category.objects.all()


def get_basket(user):
    return Basket.objects.get(user=user)


def create_product(request):
    name = request.POST.get("name")
    price = request.POST.get("price")
    description = request.POST.get("description")
    category = request.POST.get("category")
    Product.objects.create(
        name=name,
        price=price,
        description=description,
        category=Category.objects.get_or_create(name=category),
    )
