from . import views, cms
from django.urls import path

api_patterns = [
    path('cms/products', cms.products, name='cms_campaign_products'),
    path('cms/products/search', cms.product_search, name='cms_campaign_product_search'),
]

urlpatterns = [
    path('cms/banners', cms.banners, name='cms_banners'),
    path('cms/banner/add', cms.add_banner, name='cms_add_banner'),
    path('cms/banner/<int:id>/edit', cms.edit_banner, name='cms_edit_banner'),
    path('cms/banner/<int:id>/delete', cms.delete_banner, name='cms_delete_banner'),

    path('cms/campaigns', cms.campaigns, name='cms_campaigns'),
    path('cms/campaign/add', cms.add_campaign, name='cms_add_campaign'),
    path('cms/campaign/save', cms.save_campaign, name='cms_save_campaign'),
    path('cms/campaign/<int:id>/edit', cms.edit_campaign, name='cms_edit_campaign'),
    path('cms/campaign/<int:id>/update', cms.update_campaign, name='cms_update_campaign'),
    path('cms/campaign/<int:id>/delete', cms.delete_campaign, name='cms_delete_campaign'),
    
] + api_patterns