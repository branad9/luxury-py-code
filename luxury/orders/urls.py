from . import views, cms
from django.urls import path


cms_patterns = [
    path('cms/orders', cms.orders, name='cms_orders'),
    path('cms/order/<int:id>/edit', cms.edit_order, name='cms_edit_order'),
    path('cms/order-items/<int:oid>', cms.order_items, name='cms_order_items'),
    path('cms/orders/csv', cms.export_csv_orders, name='cms_export_csv_orders'),
    path('cms/order/<int:id>/delete', cms.delete_order, name='cms_delete_order'),
    path('cms/user-details/<int:uid>', cms.user_details, name='cms_user_details'), 
]


urlpatterns = [
    path('order/all', views.all_orders, name='all_orders'),
    path('order/placed', views.place_order, name='place_order'),
    path('order/cancel', views.cancel_order, name='cancel_order'),
    path('ordered', views.ordered, name='ordered'),
] + cms_patterns