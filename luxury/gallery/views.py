from django.shortcuts import render
from rest_framework import generics

from .serializers import GallerySerializer
from .pagination import GalleryPagination
from .models import Gallery

def index(request):
    gallery = Gallery.objects.all()

    return render(request, 'web/gallery/index.html', {'gallery': gallery})


class GalleryListView(generics.ListAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    pagination_class = GalleryPagination
