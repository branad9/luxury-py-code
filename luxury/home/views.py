from django.shortcuts import render
from campaigns.models import *
from django.db.models import Prefetch
from categories.models import MainCategory, Category, Brand
from products.models import Product, ProductImage
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from .models import *
from home.models import Settings
import json


def home(request):
    banners = Banner.objects.filter(active=True)
    curr_date = str(datetime.now()).replace(' ','T')
    campaigns = Campaign.objects.filter(active=True).prefetch_related(
        Prefetch('products', queryset=Product.objects.filter(active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True)))))
    context = {'banners': banners, 'campaigns': campaigns, 'curr_date':curr_date}
    return render(request, 'home/index.html', context)


def sitemap(request):
    categs = ['men-watches', 'men-bags', 'women-bags', 'women-shoes', 'women-accessories']
    main_categories = MainCategory.objects.filter(active=True).prefetch_related(
        Prefetch('categories', queryset=Category.objects.filter(slug__in=categs, active=True)), 
        Prefetch('categories__product_set', queryset=Product.objects.filter(active=True))).order_by('created')
    return render(request, 'misc/sitemap.html', {'main_categories': main_categories})    


def terms(request):
    return render(request, 'misc/terms-of-use.html')


def fcrwd(request):
    brand = get_object_or_404(Brand, slug='rolex-watches')
    category = get_object_or_404(Category, slug='men-watches')
    all_products = Product.objects.filter(brand=brand, category=category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True)))
    return render(request, 'misc/first-copy-rolex-watches-in-delhi.html', {'brand': brand, 'category': category, 'products': all_products})


def fcrmwd(request):
    brand = get_object_or_404(Brand, slug='richard-mille-watches')
    category = get_object_or_404(Category, slug='men-watches')
    all_products = Product.objects.filter(brand=brand, category=category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True)))
    return render(request, 'misc/first-copy-richard-mille-watches-in-delhi.html', {'brand': brand, 'category': category, 'products': all_products})



def fcowd(request):
    brand = get_object_or_404(Brand, slug='omega-watches')
    category = get_object_or_404(Category, slug='men-watches')
    all_products = Product.objects.filter(brand=brand, category=category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True)))
    return render(request, 'misc/first-copy-omega-watches-in-delhi.html', {'brand': brand, 'category': category, 'products': all_products})


def policy(request):
    return render(request, 'misc/privacy-policy.html')


def disclaimer(request):
    return render(request, 'misc/disclaimer.html')


def faq(request):
    return render(request, 'misc/faqs.html')


def return_exchange(request):
    return render(request, 'misc/returns-and-exchange.html')


def error_404(request, exception):
    return render(request, 'misc/404.html')


def error_500(request):
    return render(request, 'misc/500.html')
