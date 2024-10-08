from .models import Category, Product
from .form import ProductForm
from basket.models import Basket


class Crud_Product:
    @staticmethod
    def create_product(form: ProductForm, request):
        if form.is_valid():
            data = form.cleaned_data
            Product.objects.create(**data, seller=request.user)
            return True
        return False

    @staticmethod
    def delete_product(product_id):
        data = Product.objects.filter(id=product_id).delete()
        return True

    @staticmethod
    def read_product(
        product_id,
    ):
        return Product.objects.get(id=product_id)

    @staticmethod
    def get_all_products(params, limit=40):
        if params:
            prod = Product.objects.filter(category_id=params).all()[:limit]
        else:
            prod = Product.objects.all()[:limit]
        cat = Category.objects.all()[:limit]

        return prod, cat

    @staticmethod
    def add_product(request, product_id):
        product = Product.objects.get(id=product_id)
        user = request.user
        if user.is_authenticated:
            basket, created = Basket.objects.get_or_create(product=product, user=user)
            if not created:
                basket.quantity += 1
                basket.save()

        else:
            session_key = request.session.session_key
            basket, created = Basket.objects.get_or_create(
                product=product, session_key=session_key
            )
            if not created:
                basket.quantity += 1
                basket.save()
        return True
