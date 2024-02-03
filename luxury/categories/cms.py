from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.contrib import messages
from .filters import MainCategoryFilter, CategoryFilter, SubcategoryFilter
from .forms import *
from .serializers import *
import uuid


def get_maincategory_slug(instance):
    slug = slugify(instance.name)
    qs = MainCategory.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        slug = f'{slug}-{uuid.uuid4()}'
    return slug


def get_category_slug(instance):
    slug = slugify(instance.name)
    qs = Category.objects.filter(slug=slug, main_category=instance.main_category).exclude(id=instance.id)
    if qs.exists():
        slug = f'{slug}-{uuid.uuid4()}'
    return slug


def get_subcategory_slug(instance):
    slug = slugify(instance.name)
    qs = Subcategory.objects.filter(category=instance.category, slug=slug).exclude(id=instance.id)
    if qs.exists():
        slug = f'{slug}-{uuid.uuid4()}'
    return slug


def get_brand_slug(instance):
    slug = slugify(instance.name)
    qs = Brand.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        slug = f'{slug}-{uuid.uuid4()}'
    return slug


def get_tag_slug(instance):
    slug = slugify(instance.name)
    qs = Tag.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        slug = f'{slug}-{uuid.uuid4()}'
    return slug


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def main_categories(request):
    all_main_categories = MainCategory.objects.all()
    filters = MainCategoryFilter(request.GET, queryset=all_main_categories)
    filtered_main_categories = filters.qs
    paginator = Paginator(filtered_main_categories, 30)
    page = request.GET.get('page')
    paged_main_categories = paginator.get_page(page)
    context = {'main_categories': paged_main_categories, 'filters': filters}
    return render(request, 'cms/main_categories/index.html', context)


@api_view(['GET'])
def api_main_categories(request):
    all_main_categories = MainCategory.objects.all()
    serializer = MainCategorySerializer(all_main_categories, many=True)
    if serializer:
        return Response({'status': True, 'data': serializer.data})
    else:
        return Response({'status': False, 'errors': serializer.errors})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def add_main_category(request):
    if request.method == 'POST':
        form = MainCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.slug = get_maincategory_slug(f)
            f.save()
            return redirect('cms_main_categories')
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/main_categories/add.html', {'form': form})        
    else:
        form = MainCategoryForm(None)
        return render(request, 'cms/main_categories/add.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_main_category(request, id):
    try:
        item = MainCategory.objects.get(id=id)
    except MainCategory.DoesNotExist:
        return redirect('cms_main_categories')
    if request.method == 'POST':
        form = MainCategoryForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            f = form.save(commit=False)
            f.slug = get_maincategory_slug(f)
            f.save()
            return redirect('cms_main_categories')
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/main_categories/edit.html', {'form': form})        
    else:
        form = MainCategoryForm(instance=item)
        return render(request, 'cms/main_categories/edit.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_main_category(request, id):
    MainCategory.objects.filter(id=id).delete()
    return redirect('cms_main_categories')


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def categories(request):
    all_categories = Category.objects.all()
    filters = CategoryFilter(request.GET, queryset=all_categories)
    filtered_categories = filters.qs
    paginator = Paginator(filtered_categories, 30)
    page = request.GET.get('page')
    paged_categories = paginator.get_page(page)
    return render(request, 'cms/categories/index.html', {'categories': paged_categories, 'filters': filters})


@api_view(['GET'])
def api_categories(request):
    id = request.GET.get('id')
    if id is None or id == '':
        return Response({'status': False, 'data': []})
    all_categories = Category.objects.filter(main_category_id=id, active=True)
    serializer = CategorySerializer(all_categories, many=True)
    if serializer:
        return Response({'status': True, 'data': serializer.data})
    else:
        return Response({'status': False, 'errors': serializer.errors})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.slug = get_category_slug(f)
            f.save()
            return redirect('cms_categories')
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/categories/add.html', {'form': form})        
    else:
        form = CategoryForm(None)
        return render(request, 'cms/categories/add.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_category(request, id):
    try:
        item = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return redirect('cms_categories')
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            f = form.save(commit=False)
            f.slug = get_category_slug(f)
            f.save()
            return redirect('cms_categories')
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/categories/edit.html', {'form': form})        
    else:
        form = CategoryForm(instance=item)
        return render(request, 'cms/categories/edit.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_category(request, id):
    Category.objects.filter(id=id).delete()
    return redirect('cms_categories')


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def subcategories(request):
    all_subcategories = Subcategory.objects.all()
    filters = SubcategoryFilter(request.GET, queryset=all_subcategories)
    filtered_subcategories = filters.qs
    paginator = Paginator(filtered_subcategories, 30)
    page = request.GET.get('page')
    paged_categories = paginator.get_page(page)
    return render(request, 'cms/subcategories/index.html', {'subcategories': paged_categories, 'filters': filters})


@api_view(['GET'])
def api_subcategories(request):
    id = request.GET.get('id')
    if id is None or id == '':
        return Response({'status': False, 'data': []})
    all_subcategories = Subcategory.objects.filter(category_id=id, active=True)
    serializer = SubcategorySerializer(all_subcategories, many=True)
    if serializer:
        return Response({'status': True, 'data': serializer.data})
    else:
        return Response({'status': False, 'errors': serializer.errors})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def add_subcategory(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.slug = get_subcategory_slug(f)
            f.save()
            return redirect('cms_subcategories')
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/subcategories/add.html', {'form': form})        
    else:
        form = SubcategoryForm(None)
        return render(request, 'cms/subcategories/add.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_subcategory(request, id):
    try:
        item = Subcategory.objects.get(id=id)
    except Subcategory.DoesNotExist:
        return redirect('cms_subcategories')
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=item)
        if form.is_valid():
            f = form.save(commit=False)
            f.slug = get_subcategory_slug(f)
            f.save()
            return redirect('cms_subcategories')
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/subcategories/edit.html', {'form': form})        
    else:
        form = SubcategoryForm(instance=item)
        return render(request, 'cms/subcategories/edit.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_subcategory(request, id):
    Subcategory.objects.filter(id=id).delete()
    return redirect('cms_subcategories')


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def brands(request):
    all_brands = Brand.objects.all()
    paginator = Paginator(all_brands, 30)
    page = request.GET.get('page')
    paged_brands = paginator.get_page(page)
    return render(request, 'cms/brands/index.html', {'brands': paged_brands})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save()
            f.slug = get_brand_slug(f)
            f.save()
            return redirect('cms_brands')
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/brands/add.html', {'form': form})        
    else:
        form = BrandForm(None)
        return render(request, 'cms/brands/add.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_brand(request, id):
    try:
        item = Brand.objects.get(id=id)
    except Brand.DoesNotExist:
        return redirect('cms_brands')
    if request.method == 'POST':
        form = BrandForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            f = form.save()
            f.slug = get_brand_slug(f)
            f.save()
            return redirect('cms_brands')
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/brands/edit.html', {'form': form})        
    else:
        form = BrandForm(instance=item)
        return render(request, 'cms/brands/edit.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_brand(request, id):
    Brand.objects.filter(id=id).delete()
    return redirect('cms_brands')


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def tags(request):
    all_tags = Tag.objects.all()
    paginator = Paginator(all_tags, 30)
    page = request.GET.get('page')
    paged_tags = paginator.get_page(page)
    return render(request, 'cms/tags/index.html', {'tags': paged_tags})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.slug = get_tag_slug(f)
            f.save()
            return redirect('cms_tags')
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/tags/add.html', {'form': form})        
    else:
        form = TagForm(None)
        return render(request, 'cms/tags/add.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_tag(request, id):
    try:
        item = Tag.objects.get(id=id)
    except Tag.DoesNotExist:
        return redirect('cms_tags')
    if request.method == 'POST':
        form = TagForm(request.POST, instance=item)
        if form.is_valid():
            f = form.save(commit=False)
            f.slug = get_tag_slug(f)
            f.save()
            return redirect('cms_tags')
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/tags/edit.html', {'form': form})        
    else:
        form = TagForm(instance=item)
        return render(request, 'cms/tags/edit.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_tag(request, id):
    Tag.objects.filter(id=id).delete()
    return redirect('cms_tags')



@login_required
@user_passes_test(lambda user: user.is_superadmin)
def brand_contents(request):
    contents = BrandContent.objects.all()
    paginator = Paginator(contents, 30)
    page = request.GET.get('page')
    paged_contents = paginator.get_page(page)
    return render(request, 'cms/brand_contents/index.html', {'contents': paged_contents})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def add_brand_content(request):
    if request.method == 'POST':
        form = BrandContentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cms_brand_contents')
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/brand_contents/add.html', {'form': form})        
    else:
        form = BrandContentForm(None)
        return render(request, 'cms/brand_contents/add.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_brand_content(request, id):
    try:
        item = BrandContent.objects.get(id=id)
    except BrandContent.DoesNotExist:
        return redirect('cms_brand_contents')
    if request.method == 'POST':
        form = BrandContentForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('cms_brand_contents')
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/brand_contents/edit.html', {'form': form})        
    else:
        form = BrandContentForm(instance=item)
        return render(request, 'cms/brand_contents/edit.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_brand_content(request, id):
    BrandContent.objects.filter(id=id).delete()
    return redirect('cms_brand_contents')

