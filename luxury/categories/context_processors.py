from .models import MainCategory, Category, Subcategory, Brand
from products.models import Product
from django.db.models import Prefetch


def main_categories(request):
    main_categories = MainCategory.objects.filter(active=True).prefetch_related(
        Prefetch('categories', queryset=Category.objects.filter(active=True)), 
        Prefetch('categories__product_set', queryset=Product.objects.filter(active=True)), 
        Prefetch('categories__subcategories', queryset=Subcategory.objects.filter(active=True))).order_by('created')
    brands = Brand.objects.filter(active=True).prefetch_related(
        Prefetch('product_set', queryset=Product.objects.filter(active=True))).order_by('created')
    w_brands = Brand.objects.filter(category__slug='men-watches', active=True)        
    return {'cp_main_categories': main_categories, 'cp_brands': brands, 'cp_w_brands': w_brands}