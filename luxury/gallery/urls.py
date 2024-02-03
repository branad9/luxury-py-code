
from . import views, cms
from django.urls import path

cms_patterns = [
    path('cms/gallery/', cms.GalleryTempateView.as_view(), name='cms_gallery'),
    path('cms/gallery/upload-file/', cms.upload_file, name='cms_gallery_upload_file'),
    path('cms/gallery/delete-file/', cms.delete_file, name='cms_gallery_delete_file'),    
]

urlpatterns = [
    path('', views.index, name='gallery'),
    path('api/gallery', views.GalleryListView.as_view(), name='api_gallery')
]

urlpatterns += cms_patterns 