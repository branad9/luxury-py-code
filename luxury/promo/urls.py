from . import views, cms
from django.urls import path


cms_patterns = [
    path('cms/blogs', cms.blogs, name='cms_blogs'),
    path('cms/blog/add', cms.add_blog, name='cms_add_blog'),
    path('cms/blog/<int:id>/edit', cms.edit_blog, name='cms_edit_blog'),
    path('cms/blog/<int:id>/delete', cms.delete_blog, name='cms_delete_blog'),
   
    path('cms/newsletters', cms.newsletters, name='cms_newsletters'),
]

urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('<str:slug>', views.blog_details, name='blog_details'),
    path('newsletter/add', views.add_newsletter, name='add_newsletter'),
    path('api/newsletter/add', views.api_add_newsletter, name='api_add_newsletter'),
] + cms_patterns
