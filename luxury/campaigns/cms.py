from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.contrib import messages
from campaigns.serializers import *
from .forms import *
import json


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def banners(request):
    all_banners = Banner.objects.all()
    paginator = Paginator(all_banners, 30)
    page = request.GET.get('page')
    paged_banners = paginator.get_page(page)
    return render(request, 'banners/index.html', {'images': paged_banners})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def add_banner(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cms_banners')
        else:
            messages.error(request, form.errors)
            return render(request, 'banners/add.html', {'form': form})        
    else:
        form = BannerForm(None)
        return render(request, 'banners/add.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_banner(request, id):
    try:
        banner = Banner.objects.get(id=id)
    except Banner.DoesNotExist:
        return redirect('cms_banners')
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            form.save()
            return redirect('cms_banners')
        else:
            messages.error(request, form.errors)
            return render(request, 'banners/edit.html', {'form': form})        
    else:
        form = BannerForm(instance=banner)
        return render(request, 'banners/edit.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_banner(request, id):
    Banner.objects.filter(id=id).delete()
    return redirect('cms_banners')


@api_view(['GET'])
def products(request):   
    all_products = Product.objects.filter(active=True)
    paginator = PageNumberPagination()
    paginator.page_size = 15
    products_pages = paginator.paginate_queryset(all_products, request)
    serializer = ProductSerializer(products_pages, many=True)
    if serializer:
        return Response({'status': True, 'data': serializer.data, 'prev': paginator.get_previous_link(), 
                         'next': paginator.get_next_link()})
    else:
        return Response({'status': False, 'errors': serializer.errors})


@api_view(['GET'])
def product_search(request):
    search_text = request.GET.get('search')
    if search_text is not None and search_text != '':
        products = Product.objects.filter(name__icontains=search_text, active=True)
    else:
        products = Product.objects.filter(active=True)
    paginator = PageNumberPagination()
    paginator.page_size = 15
    product_pages = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(product_pages, many=True)
    if serializer:
        return Response({'status': True, 'data': serializer.data, 'prev': paginator.get_previous_link(), 
                         'next': paginator.get_next_link()})
    else:
        return Response({'status': False, 'errors': serializer.errors})         


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def campaigns(request):
    all_campaigns = Campaign.objects.all()
    paginator = Paginator(all_campaigns, 30)
    page = request.GET.get('page')
    paged_campaigns = paginator.get_page(page)
    return render(request, 'campaigns/index.html', {'campaigns': paged_campaigns})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def add_campaign(request):
    return render(request, 'campaigns/add.html')


@api_view(['POST'])
@login_required
@user_passes_test(lambda user: user.is_superadmin)
def save_campaign(request):
    json_campaign = request.POST.get('campaign')
    image = request.FILES.get('image')
    campaign = json.loads(json_campaign)
    data = {'title': campaign['title'], 'subtitle': campaign['subtitle'],
            'products': campaign['products'], 'active': campaign['active']}
    if image is not None and image != '':
        data['image'] = image        
    serializer = CampaignSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': True})
    else:
        return Response({'status': False, 'errors': serializer.errors})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_campaign(request, id):
    campaign_obj = get_object_or_404(Campaign, id=id)
    serializer = CampaignSerializer(campaign_obj)
    if serializer:
        campaign = json.dumps(serializer.data)
    else:
        campaign = None
    return render(request, 'campaigns/edit.html', {'campaign': campaign, 'id': id})


@api_view(['POST'])
@login_required
@user_passes_test(lambda user: user.is_superadmin)
def update_campaign(request, id):
    try:
        campaign_obj = Campaign.objects.get(id=id)
    except Campaign.DoesNotExist:
        return Response({'status': False, 'errors': {"Error": ["Campaign not found."]}})
    json_campaign = request.POST.get('campaign')
    image = request.FILES.get('image')
    campaign = json.loads(json_campaign)
    print(f'products are {campaign}')
    data = {'title': campaign['title'], 'subtitle': campaign['subtitle'],
            'products': campaign['products'], 'active': campaign['active']}
    if image is not None and image != '':
        data['image'] = image           
    serializer = CampaignSerializer(campaign_obj, partial=True, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': True})
    else:
        return Response({'status': False, 'errors': serializer.errors})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_campaign(request, id):
    Campaign.objects.filter(id=id).delete()
    return redirect('cms_campaigns')
