from django.db import models
from home.models import SoftDeleteModel
from products.models import Product


class Banner(SoftDeleteModel):
    title = models.CharField(max_length=100, null=True, blank=True)
    subtitle = models.CharField(max_length=250, null=True, blank=True)
    background_image = models.ImageField(upload_to='images/banners')
    image_left = models.ImageField(upload_to='images/banners')
    image_right = models.ImageField(upload_to='images/banners')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Banners'
        ordering = ['-created'] 


class Campaign(SoftDeleteModel):
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='images/campaigns', null=True, blank=True)  
    products = models.ManyToManyField(Product)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Campaigns'
        ordering = ['-created'] 
