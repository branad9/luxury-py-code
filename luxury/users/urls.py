from . import views, cms
from django.urls import path

api_patterns = [
    path('api/users/', cms.api_users, name='api_users'),
    path('api/addresses/', views.api_get_addresses, name='api_get_addresses'),
    path('api/address/details', views.api_address_details, name='api_address_details'),
    path('api/address/add', views.api_add_address, name='api_add_address'),
    path('api/address/edit', views.api_edit_address, name='api_edit_address'),
    path('api/address/delete', views.api_delete_address, name='api_delete_address'),
    path('api/address/default', views.api_address_change_default, name='api_address_change_default'),
]


cms_patterns = [
    path('cms/login/', cms.user_login, name='cms_login'),
    path('cms/logout/', cms.user_logout, name='cms_logout'),
    path('cms/forgot_password', cms.forgot_password, name='cms_forgot_password'),
    path('cms/resetpassword_validate/<uidb64>/<token>', cms.reset_password_validate, name='cms_reset_password_validate'),
    path('cms/resetpassword/', cms.reset_password, name='cms_reset_password'),
    path('cms/change_password/<int:id>', cms.change_password, name='cms_change_password'),

    path('cms/users', cms.users, name='cms_users'),
    path('cms/customers', cms.customers, name='cms_customers'),
    path('cms/customers/cron', cms.cron_new_customers, name='cron_customers'),
    path('cms/customers/csv', cms.export_csv_customers, name='cms_export_csv_customers'),
    path('cms/user/add', cms.add_user, name='cms_add_user'),
    path('cms/user/<int:id>/edit', cms.edit_user, name='cms_edit_user'),
    path('cms/customer/<int:id>/edit', cms.edit_customer, name='cms_edit_customer'),
    path('cms/user/<int:id>/delete', cms.delete_user, name='cms_delete_user'),
    
]


urlpatterns = [
    path('login', views.user_login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.user_logout, name='logout'),
    path('verify-phone', views.verify_phone, name='verify_phone'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('forgot-password', views.forgot_password, name='forgot_password'),
    path('resetpassword_validate/<uidb64>/<token>', views.reset_password_validate, name='reset_password_validate'),
    path('reset-password', views.reset_password, name='reset_password'),

    path('user-dashboard', views.user_dashboard, name='user_dashboard'),

    path('wishlist', views.wishlist, name='wishlist'),
    path('wishlist/api', views.get_wishlist, name='get_wishlist'),
    path('wishlist/add', views.add_wishlist, name='add_wishlist'),
    path('wishlist/delete', views.delete_wishlist, name='delete_wishlist'),

] + cms_patterns + api_patterns

