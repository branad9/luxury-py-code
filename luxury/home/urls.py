from . import views, cms
from django.urls import path


cms_patterns = [
    path('cms', cms.home, name='cms_home'),
    path('cms/settings', cms.settings, name='cms_settings'),
    path('cms/settings/change', cms.change_settings, name='cms_change_settings'),
]

urlpatterns = [
    path('', views.home, name='home'),
    path('sitemap', views.sitemap, name='sitemap'),
    path('terms-of-use', views.terms, name='terms'),
    path('first-copy-rolex-watches-in-delhi', views.fcrwd, name='fcrwd'),
    path('first-copy-richard-mille-watches-in-delhi', views.fcrmwd, name='fcrmwd'),
    path('first-copy-omega-watches-in-delhi', views.fcowd, name='fcowd'),
    path('privacy-policy', views.policy, name='policy'),
    path('disclaimer', views.disclaimer, name='disclaimer'),
    path('faqs', views.faq, name='faq'),
    path('returns-and-exchange', views.return_exchange, name='return_exchange'),
] + cms_patterns
