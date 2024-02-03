from . import views, cms
from django.urls import path


cms_patterns = [
    path('cms/cart', cms.cart, name='cms_cart'),   
    path('cms/send-message/<int:uid>', cms.send_msg, name='cms_send_msg'), 
    path('cms/cart/<int:id>/delete', cms.delete_cart, name='cms_delete_cart'),
    path('cms/cart/csv', cms.export_csv_cart, name='cms_export_csv_cart'),   
]

api_patterns = [
    path('api/cart/change', views.change_cart, name='change_cart'),   
    path('api/cart/delete', views.delete_cart, name='delete_cart'),   
    path('api/cart', views.get_cart, name='get_cart'),  
    path('cron/orphancarts', views.cron_orphan_carts, name='cron_orphan_carts'),
]


urlpatterns = [
    path('', views.cart, name='cart'),
] + api_patterns + cms_patterns

