from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Blog, Newsletter
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NewsletterSerializer


def blogs(request):
    blogs = Blog.objects.filter(active=True)
    paginator = Paginator(blogs, per_page=24)
    paged_blogs = paginator.get_page(1)
    paged_blogs.adjusted_elided_pages = paginator.get_elided_page_range(1)
    return render(request, 'web/blogs/index.html', {'blogs': paged_blogs})    


def blog_details(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    rel_blogs = Blog.objects.filter(active=True).exclude(slug=slug)[:6]
    return render(request, 'web/blogs/blog.html', {'blog': blog, 'rel_blogs': rel_blogs})    


def add_newsletter(request):
    if request.method == 'POST':
        email = request.POST['email']
        nl = Newsletter.objects.create(email=email)
        if nl:
            messages.success(request, 'Newsletter submitted successfully.')  
        else:      
            messages.error(request, 'Failed to submit newsletter.')  
    return redirect('home')
    
    
@api_view(['POST'])
def api_add_newsletter(request):
    email = request.POST.get('email')
    data = {'email': email}
    serializer = NewsletterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': True})
    else:
        return Response({'status': False, 'errors': serializer.errors})