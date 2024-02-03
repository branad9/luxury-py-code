from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import Blog, BlogForm, Newsletter
from datetime import datetime
import uuid


def get_blog_slug(instance):
    slug = slugify(instance.name)
    qs = Blog.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        slug = f'{slug}-{uuid.uuid4()}'
    return slug


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def blogs(request):
    blogs = Blog.objects.order_by('-created')
    paginator = Paginator(blogs, 20)
    page = request.GET.get('page')
    paged_blogs = paginator.get_page(page)
    return render(request, 'cms/blogs/index.html', {'blogs': paged_blogs})    


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.slug = get_blog_slug(f)
            f.save()
            return redirect('cms_blogs')
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/blogs/add.html', {'form': form})
    else:
        form = BlogForm(None)
        return render(request, 'cms/blogs/add.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def edit_blog(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        return redirect('cms_blogs')
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            f = form.save(commit=False)
            f.slug = get_blog_slug(f)
            f.save()
            return redirect('cms_blogs')
        else:
            messages.error(request, form.errors)
            return render(request, 'cms/blogs/edit.html', {'form': form})
    else:
        form = BlogForm(instance=blog)
        return render(request, 'cms/blogs/edit.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.is_superadmin)
def delete_blog(request, id):
    try:
        blog = Blog.objects.get(id=id)
        blog.deleted = datetime.now()
        blog.save()
    except Blog.DoesNotExist:
        pass    
    return redirect('cms_blogs')
    
    
@login_required
@user_passes_test(lambda user: user.is_superadmin)
def newsletters(request):
    letters = Newsletter.objects.all()
    paginator = Paginator(letters, 20)
    page = request.GET.get('page')
    paged_letters = paginator.get_page(page)
    return render(request, 'cms/newsletters/index.html', {'newsletters': paged_letters})
