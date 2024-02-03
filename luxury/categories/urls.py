from . import views, cms
from django.urls import path


api_patterns = [
    path('cms/main_categories/api', cms.api_main_categories, name='api_main_categories'),
    path('cms/categories/api', cms.api_categories, name='api_categories'),
    path('cms/subcategories/api', cms.api_subcategories, name='api_subcategories'),
]

urlpatterns = [
    path('cms/main_categories', cms.main_categories, name='cms_main_categories'),
    path('cms/main_categories/add', cms.add_main_category, name='cms_add_main_category'),
    path('cms/main_categories/<int:id>/edit', cms.edit_main_category, name='cms_edit_main_category'),
    path('cms/main_categories/<int:id>/delete', cms.delete_main_category, name='cms_delete_main_category'),
    
    path('cms/categories', cms.categories, name='cms_categories'),
    path('cms/category/add', cms.add_category, name='cms_add_category'),
    path('cms/category/<int:id>/edit', cms.edit_category, name='cms_edit_category'),
    path('cms/category/<int:id>/delete', cms.delete_category, name='cms_delete_category'),
    
    path('cms/subcategories', cms.subcategories, name='cms_subcategories'),
    path('cms/subcategory/add', cms.add_subcategory, name='cms_add_subcategory'),
    path('cms/subcategory/<int:id>/edit', cms.edit_subcategory, name='cms_edit_subcategory'),
    path('cms/subcategory/<int:id>/delete', cms.delete_subcategory, name='cms_delete_subcategory'),
    
    path('cms/brands', cms.brands, name='cms_brands'),
    path('cms/brand/add', cms.add_brand, name='cms_add_brand'),
    path('cms/brand/<int:id>/edit', cms.edit_brand, name='cms_edit_brand'),
    path('cms/brand/<int:id>/delete', cms.delete_brand, name='cms_delete_brand'),
    
    path('cms/tags', cms.tags, name='cms_tags'),
    path('cms/tag/add', cms.add_tag, name='cms_add_tag'),
    path('cms/tag/<int:id>/edit', cms.edit_tag, name='cms_edit_tag'),
    path('cms/tag/<int:id>/delete', cms.delete_tag, name='cms_delete_tag'),
    
    path('cms/brand_contents', cms.brand_contents, name='cms_brand_contents'),
    path('cms/brand_content/add', cms.add_brand_content, name='cms_add_brand_content'),
    path('cms/brand_content/<int:id>/edit', cms.edit_brand_content, name='cms_edit_brand_content'),
    path('cms/brand_content/<int:id>/delete', cms.delete_brand_content, name='cms_delete_brand_content'),
    
] + api_patterns