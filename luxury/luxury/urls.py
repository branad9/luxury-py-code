from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from products.models import HomeSitemap, ProductSitemap, ProductImageSitemap
from promo.models import BlogSitemap    
from categories.models import CategorySitemap, SubcategorySitemap


urlpatterns = [
    path('warp/', admin.site.urls),
    path('', include('home.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': {'home': HomeSitemap, 'category': CategorySitemap, 'subcategory': SubcategorySitemap, 'blog': BlogSitemap}},
            name='django.contrib.sitemaps.views.sitemap'),
    path(
        "sitemap_images.xml",
        sitemap,
        {"sitemaps": {"images": ProductImageSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path('product-sitemap.xml', sitemap, {'sitemaps': {'Product': ProductSitemap}},
            name='django.contrib.sitemaps.views.sitemap'),
    path('campaigns/', include('campaigns.urls')),
    path('user/', include('users.urls')),
    path('categories/', include('categories.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('blogs/', include('promo.urls')),
    path('gallery/', include('gallery.urls')),
    path('integrations/', include('integrations.urls')),
    path('misc/', include("misc.urls")),
    path('', include('products.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  


handler404 = 'home.views.error_404'
handler500 = 'home.views.error_500'
