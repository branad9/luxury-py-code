from django.shortcuts import render, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Prefetch, Q
from rest_framework import status
from .serializers import *
from .models import *
from home.models import Settings
import json


@api_view(['GET'])
def get_attributes(request):
    json_ids = request.GET.get('ids')
    ids = json.loads(json_ids)
    if ids is None or ids == '':
        attributes = Attribute.objects.filter(active=True)
    else:
        attributes = Attribute.objects.filter(id__in=ids, active=True)
    serializer = ReadAttributeSerializer(attributes, many=True)
    if serializer:
        return Response({'status': True, 'data': serializer.data})
    else:
        errors = {}
        for field_name, field_errors in serializer.errors.items():
            errors[field_name] = field_errors[0]
        return Response({'status': False, 'errors': errors})    


@api_view(['GET'])
def get_products(request):
    sort = request.GET.get('sort')
    min = request.GET.get('min')
    max = request.GET.get('max')
    if sort is None or sort == '':
        all_products = Product.objects.filter(active=True)
    else:
        all_products = Product.objects.filter(active=True).order_by(sort)   
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)

    paginator = PageNumberPagination()
    paginator.page_size = 24
    product_pages = paginator.paginate_queryset(all_products, request)
    serializer = WebProductSerializer(product_pages, many=True)
    product_pages = {'paging': paginator.page.has_other_pages(), 'current': paginator.page.number, 
        'count': paginator.page.paginator.num_pages, 'prev': paginator.page.has_previous() or None, 'next': paginator.page.has_next()}
    if serializer:
        return Response({'status': True, 'data': serializer.data, 'pages': product_pages})
    else:
        errors = {}
        for field_name, field_errors in serializer.errors.items():
            errors[field_name] = field_errors[0]
        return Response({'status': False, 'errors': errors})    


@api_view(['GET'])
def get_category_products(request, cid):
    sort = request.GET.get('sort')
    min = request.GET.get('min')
    max = request.GET.get('max')
    if sort is None or sort == '':
        all_products = Product.objects.filter(category_id=cid, active=True)
    else:
        all_products = Product.objects.filter(category_id=cid, active=True).order_by(sort)    
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)    

    paginator = PageNumberPagination()
    paginator.page_size = 24
    product_pages = paginator.paginate_queryset(all_products, request)
    serializer = WebProductSerializer(product_pages, many=True)
    product_pages = {'paging': paginator.page.has_other_pages(), 'current': paginator.page.number, 
        'count': paginator.page.paginator.num_pages, 'prev': paginator.page.has_previous() or None, 'next': paginator.page.has_next()}
    if serializer:
        return Response({'status': True, 'data': serializer.data, 'pages': product_pages})
    else:
        errors = {}
        for field_name, field_errors in serializer.errors.items():
            errors[field_name] = field_errors[0]
        return Response({'status': False, 'errors': errors})    


@api_view(['GET'])
def get_subcategory_products(request, scid):
    sort = request.GET.get('sort')
    min = request.GET.get('min')
    max = request.GET.get('max')
    if sort is None or sort == '':
        all_products = Product.objects.filter(subcategory_id=scid, active=True)
    else:
        all_products = Product.objects.filter(subcategory_id=scid, active=True).order_by(sort)    
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)    

    paginator = PageNumberPagination()
    paginator.page_size = 24
    product_pages = paginator.paginate_queryset(all_products, request)
    serializer = WebProductSerializer(product_pages, many=True)
    product_pages = {'paging': paginator.page.has_other_pages(), 'current': paginator.page.number, 
        'count': paginator.page.paginator.num_pages, 'prev': paginator.page.has_previous() or None, 'next': paginator.page.has_next()}
    if serializer:
        return Response({'status': True, 'data': serializer.data, 'pages': product_pages})
    else:
        errors = {}
        for field_name, field_errors in serializer.errors.items():
            errors[field_name] = field_errors[0]
        return Response({'status': False, 'errors': errors})    


@api_view(['GET'])
def get_brand_products(request, bid):
    sort = request.GET.get('sort')
    min = request.GET.get('min')
    max = request.GET.get('max')
    if sort is None or sort == '':
        all_products = Product.objects.filter(brand_id=bid, active=True)
    else:
        all_products = Product.objects.filter(brand_id=bid, active=True).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)    

    paginator = PageNumberPagination()
    paginator.page_size = 24
    product_pages = paginator.paginate_queryset(all_products, request)
    serializer = WebProductSerializer(product_pages, many=True)
    product_pages = {'paging': paginator.page.has_other_pages(), 'current': paginator.page.number, 
        'count': paginator.page.paginator.num_pages, 'prev': paginator.page.has_previous() or None, 'next': paginator.page.has_next()}
    if serializer:
        return Response({'status': True, 'data': serializer.data, 'pages': product_pages})
    else:
        errors = {}
        for field_name, field_errors in serializer.errors.items():
            errors[field_name] = field_errors[0]
        return Response({'status': False, 'errors': errors})    


@api_view(['GET'])
def api_search_products(request):
    search = request.GET.get('productSearch')
    if search is not None and search != '':
        all_products = Product.objects.filter(name__icontains=search, active=True)
        paginator = PageNumberPagination()
        paginator.page_size = 24
        user_pages = paginator.paginate_queryset(all_products, request)
        serializer = WebProductSerializer(user_pages, many=True)
        product_pages = {'paging': paginator.page.has_other_pages(), 'current': paginator.page.number, 
            'count': paginator.page.paginator.num_pages, 'prev': paginator.page.has_previous() or None, 'next': paginator.page.has_next()}
    else:
        all_products = Product.objects.filter(active=True)
        paginator = PageNumberPagination()
        paginator.page_size = 24
        user_pages = paginator.paginate_queryset(all_products, request)
        serializer = WebProductSerializer(user_pages, many=True)
        product_pages = {'paging': paginator.page.has_other_pages(), 'current': paginator.page.number, 
            'count': paginator.page.paginator.num_pages, 'prev': paginator.page.has_previous() or None, 'next': paginator.page.has_next()}       
    if serializer:
        return Response({'status': True, 'data': serializer.data, 'pages': product_pages})
    else:
        errors = {}
        for field_name, field_errors in serializer.errors.items():
            errors[field_name] = field_errors[0]
        return Response({'status': False, 'errors': errors})    


def search_products(request):
    sort = request.GET.get('sort') or '-created'
    search = request.GET.get('search')
    if search is not None and search != '':
        all_products = Product.objects.filter(Q(name__icontains=search) | Q(slug__icontains=search), active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)
    else:    
        all_products = Product.objects.filter(active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)
    paginator = Paginator(all_products, 24)
    paged_products = paginator.get_page(1)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(1)
    return render(request, 'web/searched-products.html', {'products': paged_products})


def paged_search_products(request, page):
    sort = request.GET.get('sort') or '-created'
    search = request.GET.get('search')
    if search is not None and search != '':
        all_products = Product.objects.filter(Q(name__icontains=search) | Q(slug__icontains=search), active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)
    else:    
        all_products = Product.objects.filter(active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)
    paginator = Paginator(all_products, 24)
    paged_products = paginator.get_page(page)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(page)
    return render(request, 'web/searched-products.html', {'products': paged_products})


def products(request):
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('minprice')
    max = request.GET.get('maxprice')
    all_products = Product.objects.filter(active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)   
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(1)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(1)
    return render(request, 'web/products-list.html', {'products': paged_products})


def paged_products(request, page):
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('minprice')
    max = request.GET.get('maxprice')
    all_products = Product.objects.filter(active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort) 
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(page)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(page)
    return render(request, 'web/products-list.html', {'products': paged_products})


def sort_products(request):
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('min')
    max = request.GET.get('max')
    all_products = Product.objects.filter(active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, 24)
    paged_products = paginator.get_page(1)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(1)
    return render(request, 'web/partials/sorted-products.html', {'products': paged_products})    


def paged_sort_products(request, page):
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('min')
    max = request.GET.get('max')
    all_products = Product.objects.filter(active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(page)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(page)
    return render(request, 'web/partials/sorted-products.html', {'products': paged_products})    


def maincategory_products(request, mcslug):
    main_category = get_object_or_404(MainCategory, slug=mcslug)
    categories = Category.objects.filter(main_category=main_category, active=True)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('minprice')
    max = request.GET.get('maxprice')
    all_products = Product.objects.filter(main_category=main_category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort) 
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(1)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(1)
    return render(request, 'web/maincategory-products.html', {'main_category': main_category, 'categories': categories, 'products': paged_products})


def paged_maincategory_products(request, mcslug, page):
    main_category = get_object_or_404(MainCategory, slug=mcslug)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('minprice')
    max = request.GET.get('maxprice')
    all_products = Product.objects.filter(main_category=main_category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(page)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(page)
    return render(request, 'web/maincategory-products.html', {'main_category': main_category, 'products': paged_products})


def sort_maincategory_products(request, mcslug):
    main_category = get_object_or_404(MainCategory, slug=mcslug)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('min')
    max = request.GET.get('max')
    all_products = Product.objects.filter(main_category=main_category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, 24)
    paged_products = paginator.get_page(1)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(1)
    return render(request, 'web/partials/sorted-maincategory-products.html', {'main_category': main_category, 'products': paged_products})    


def paged_sort_maincategory_products(request, mcslug, page):
    main_category = get_object_or_404(MainCategory, slug=mcslug)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('min')
    max = request.GET.get('max')
    all_products = Product.objects.filter(main_category=main_category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(page)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(page)
    return render(request, 'web/partials/sorted-maincategory-products.html', {'main_category': main_category, 'products': paged_products}) 


def category_products(request, mcslug, cslug):
    main_category = get_object_or_404(MainCategory, slug=mcslug)
    category = get_object_or_404(Category, main_category=main_category, slug=cslug)
    brands = Brand.objects.filter(category=category, active=True).prefetch_related(Prefetch('product_set', queryset=Product.objects.filter(category=category, active=True)))
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('minprice')
    max = request.GET.get('maxprice')
    all_products = Product.objects.filter(category=category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(1)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(1)

    return render(request, 'web/category-products.html', {'brands': brands, 'category': category, 'products': paged_products, 'main_category': category.main_category})


def paged_category_products(request, mcslug, cslug, page):
    main_category = get_object_or_404(MainCategory, slug=mcslug)
    category = get_object_or_404(Category, main_category=main_category, slug=cslug)
    brands = Brand.objects.filter(category=category, active=True).prefetch_related(Prefetch('product_set', queryset=Product.objects.filter(category=category, active=True)))
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('minprice')
    max = request.GET.get('maxprice')
    all_products = Product.objects.filter(category=category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort) 
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(page)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(page)
    return render(request, 'web/category-products.html', {'brands': brands, 'category': category, 'products': paged_products, 'main_category': category.main_category})


def sort_category_products(request, mcslug, cslug):
    main_category = get_object_or_404(MainCategory, slug=mcslug)
    category = get_object_or_404(Category, main_category=main_category, slug=cslug)
    brands = Brand.objects.filter(category=category, active=True)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('min')
    max = request.GET.get('max')
    all_products = Product.objects.filter(category=category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, 24)
    paged_products = paginator.get_page(1)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(1)
    return render(request, 'web/partials/sorted-category-products.html', {'brands': brands, 'category': category, 'products': paged_products, 'main_category': category.main_category})    


def paged_sort_category_products(request, mcslug, cslug, page):
    main_category = get_object_or_404(MainCategory, slug=mcslug)
    category = get_object_or_404(Category, main_category=main_category, slug=cslug)
    brands = Brand.objects.filter(category=category, active=True)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('min')
    max = request.GET.get('max')
    all_products = Product.objects.filter(category=category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(page)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(page)
    return render(request, 'web/partials/sorted-category-products.html', {'brands': brands, 'category': category, 'products': paged_products, 'main_category': category.main_category})   


def subcategory_products(request, mcslug, cslug, scslug):
    main_category = get_object_or_404(MainCategory, slug=mcslug)
    category = get_object_or_404(Category, main_category=main_category, slug=cslug, active=True)
    subcategory = get_object_or_404(Subcategory, category=category, slug=scslug, active=True)
    brands = Brand.objects.filter(category=category, active=True).prefetch_related(Prefetch('product_set', queryset=Product.objects.filter(category=category, active=True)))
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('minprice')
    max = request.GET.get('maxprice')
    all_products = Product.objects.filter(subcategory=subcategory, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max) 
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(1)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(1)
    context = {'brands': brands, 'category': category, 'subcategory': subcategory, 'products': paged_products, 'main_category': category.main_category}
    return render(request, 'web/subcategory-products.html', context)


def paged_subcategory_products(request, mcslug, cslug, scslug, page):
    main_category = get_object_or_404(MainCategory, slug=mcslug)
    category = get_object_or_404(Category, main_category=main_category, slug=cslug, active=True)
    subcategory = get_object_or_404(Subcategory, category=category, slug=scslug, active=True)
    brands = Brand.objects.filter(category=category, active=True).prefetch_related(Prefetch('product_set', queryset=Product.objects.filter(category=category, active=True)))
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('minprice')
    max = request.GET.get('maxprice')
    all_products = Product.objects.filter(subcategory=subcategory, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort) 
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max) 
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(page)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(page)
    context = {'brands': brands, 'category': category, 'subcategory': subcategory, 'products': paged_products, 'main_category': category.main_category}
    return render(request, 'web/subcategory-products.html', context)


def sort_subcategory_products(request, mcslug, cslug, scslug):
    main_category = get_object_or_404(MainCategory, slug=mcslug)
    category = get_object_or_404(Category, main_category=main_category, slug=cslug, active=True)
    subcategory = get_object_or_404(Subcategory, category=category, slug=scslug, active=True)
    brands = Brand.objects.filter(category=category, active=True)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('min')
    max = request.GET.get('max')
    all_products = Product.objects.filter(subcategory=subcategory, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, 24)
    paged_products = paginator.get_page(1)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(1)
    context = {'brands': brands, 'category': category, 'subcategory': subcategory, 'products': paged_products, 'main_category': category.main_category}
    return render(request, 'web/partials/sorted-subcategory-products.html', context)    


def paged_sort_subcategory_products(request, mcslug, cslug, scslug, page):
    main_category = get_object_or_404(MainCategory, slug=mcslug)
    category = get_object_or_404(Category, main_category=main_category, slug=cslug, active=True)
    subcategory = get_object_or_404(Subcategory, category=category, slug=scslug, active=True)
    brands = Brand.objects.filter(category=category, active=True)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('min')
    max = request.GET.get('max')
    all_products = Product.objects.filter(subcategory=subcategory, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(page)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(page)
    context = {'brands': brands, 'category': category, 'subcategory': subcategory, 'products': paged_products, 'main_category': category.main_category}
    return render(request, 'web/partials/sorted-subcategory-products.html', context)   


def main_brand_products(request, bslug):
    brand = get_object_or_404(Brand, slug=bslug)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('minprice')
    max = request.GET.get('maxprice')
    all_products = Product.objects.filter(brand=brand, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort) 
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max) 
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(1)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(1)
    return render(request, 'web/main-brands-products.html', {'brand': brand, 'products': paged_products})


def paged_main_brand_products(request, bslug, page):
    brand = get_object_or_404(Brand, slug=bslug)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('minprice')
    max = request.GET.get('maxprice')
    all_products = Product.objects.filter(brand=brand, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)   
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max) 
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(page)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(page)
    return render(request, 'web/main-brands-products.html', {'brand': brand, 'products': paged_products})


def sort_main_brand_products(request, bslug):
    brand = get_object_or_404(Brand, slug=bslug)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('min')
    max = request.GET.get('max')
    all_products = Product.objects.filter(brand=brand, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, 24)
    paged_products = paginator.get_page(1)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(1)
    return render(request, 'web/partials/sorted-main-brands-products.html', {'brand': brand, 'products': paged_products})    


def paged_sort_main_brand_products(request, bslug, page):
    brand = get_object_or_404(Brand, slug=bslug)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('min')
    max = request.GET.get('max')
    all_products = Product.objects.filter(brand=brand, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(page)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(page)
    return render(request, 'web/partials/sorted-main-brands-products.html', {'brand': brand, 'products': paged_products}) 


def brand_products(request, cslug, bslug):
    brand = get_object_or_404(Brand, slug=bslug)
    category = get_object_or_404(Category, slug=cslug)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('minprice')
    max = request.GET.get('maxprice')
    all_products = Product.objects.filter(brand=brand, category=category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)   
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(1)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(1)
    try: 
        bc = BrandContent.objects.get(category=category, brand=brand)
    except BrandContent.DoesNotExist:
        bc = None
    return render(request, 'web/brands-products.html', {'brand': brand, 'category': category, 'products': paged_products, 'brand_content': bc})


def paged_brand_products(request, cslug, bslug, page):
    brand = get_object_or_404(Brand, slug=bslug)
    category = get_object_or_404(Category, slug=cslug)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('minprice')
    max = request.GET.get('maxprice')
    all_products = Product.objects.filter(brand=brand, category=category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max) 
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(page)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(page)
    try: 
        bc = BrandContent.objects.get(category=category, brand=brand)
    except BrandContent.DoesNotExist:
        bc = None
    return render(request, 'web/brands-products.html', {'brand': brand, 'category': category, 'products': paged_products, 'brand_content': bc})


def sort_brand_products(request, cslug, bslug):
    brand = get_object_or_404(Brand, slug=bslug)
    category = get_object_or_404(Category, slug=cslug)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('min')
    max = request.GET.get('max')
    all_products = Product.objects.filter(brand=brand, category=category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, 24)
    paged_products = paginator.get_page(1)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(1)
    return render(request, 'web/partials/sorted-brands-products.html', {'brand': brand, 'category': category, 'products': paged_products})    


def paged_sort_brand_products(request, cslug, bslug, page):
    brand = get_object_or_404(Brand, slug=bslug)
    category = get_object_or_404(Category, slug=cslug)
    sort = request.GET.get('sort') or '-created'
    min = request.GET.get('min')
    max = request.GET.get('max')
    all_products = Product.objects.filter(brand=brand, category=category, active=True).prefetch_related(Prefetch('images', queryset=ProductImage.objects.filter(default=True))).order_by(sort)  
    if min is not None and min != '':
        all_products = all_products.filter(price__gte=min)
    if max is not None and max != '':
        all_products = all_products.filter(price__lte=max)
    paginator = Paginator(all_products, per_page=24)
    paged_products = paginator.get_page(page)
    paged_products.adjusted_elided_pages = paginator.get_elided_page_range(page)
    return render(request, 'web/partials/sorted-brands-products.html', {'brand': brand, 'category': category, 'products': paged_products}) 


def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug)
    serializer = WebProductSerializer(product)
    suggested_products = Product.objects.filter(category=product.category, active=True).exclude(id=product.id).order_by('created')[:5]
    suggested_products_serializer = WebProductSerializer(suggested_products, many=True)
    authed = request.user.is_authenticated
    settings = Settings.objects.all().first()
    # image_url = request.build_absolute_uri(product.images.all.url)
    context = {'pproduct': product, 'product': json.dumps(serializer.data), 'suggested_products': json.dumps(suggested_products_serializer.data), 'authed': json.dumps(authed), 'settings': settings}
    return render(request, 'web/product-details.html', context)


@api_view(['POST'])
def api_product_enquiry(request):
    serializer = ProductEnquirySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)