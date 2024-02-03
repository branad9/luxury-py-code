from email.policy import default
from django.db import models
from categories.models import *
from home.models import SoftDeleteModel
from sorl.thumbnail import ImageField
from django.contrib.sitemaps import Sitemap
from datetime import datetime, timedelta
from django.core.validators import RegexValidator
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files import File
from PIL import Image
from io import BytesIO

phone_validator = RegexValidator(r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$', message="Invalid phone number")

def upload_to(instance, filename, upload_dir):
    extension = filename.split('.')[-1]
    new_filename = f'{instance.name}.{extension}'
    return os.path.join(upload_dir, new_filename)

def image_upload_to(instance, filename):
    return upload_to(instance, filename, 'images/products')

def cmp_image_upload_to(instance, filename):
    return upload_to(instance, filename, 'images/cmpproducts')

def rename_file(self, original, upload_to):
        file_path = original.image.path
        new_file_path = default_storage.get_available_name(upload_to(self, self.image.name))
        in_memory_file = ContentFile(original.image.read())
        default_storage.delete(file_path)
        default_storage.save(new_file_path, in_memory_file)
        self.image.name = new_file_path

def reduce_image_size(image):
    img = Image.open(image)
    thumb_io = BytesIO()
    img.save(thumb_io, 'jpeg', quality=30, optimize=True)
    new_image = File(thumb_io, name=image.name)
    return new_image


class Product(SoftDeleteModel):
    TYPE_CHOICES = (
        ('Simple', 'Simple'),
        ('Variable', 'Variable'),
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    code = models.CharField(max_length=250)
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    tag = models.ManyToManyField(Tag, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    reference = models.URLField(null=True, blank=True)
    opening_qty = models.IntegerField(null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    length = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    pre_order = models.BooleanField(default=False)
    pre_order_date = models.DateField(null=True, blank=True)
    pre_order_msg = models.CharField(max_length=250, null=True, blank=True)
    type = models.CharField(max_length=9, choices=TYPE_CHOICES, default='Simple')
    specs = models.JSONField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    schema = models.TextField(null=True, blank=True)
    robots = models.CharField(max_length=255, null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ['-id'] 

    def __str__(self):
        return self.name     


class ProductImage(SoftDeleteModel):
    image = ImageField(upload_to=image_upload_to)
    cmp_image = ImageField(upload_to=cmp_image_upload_to, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    default = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    alt = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Product Images'
        ordering = ['-created']
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                condition=models.Q(deleted=None),
                name='unique_name')
        ]
    
    def save(self, *args, **kwargs):
        if self.pk:
            # get the original instance from the database
            original = ProductImage.objects.get(pk=self.pk)

            # if the name or image has changed
            if  self.name != original.name or self.image != original.image:
                # update the image filename
                rename_file(self, original, image_upload_to)

                # update cmp_image filename
                default_storage.delete(original.cmp_image.path)
                self.cmp_image = reduce_image_size(self.image)
        else:
            self.cmp_image = reduce_image_size(self.image)

        super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.image}' 


class Attribute(SoftDeleteModel):
    name = models.CharField(max_length=250)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Attributes'
        ordering = ['-created']

    def __str__(self):
        return self.name    


class AttributeValue(SoftDeleteModel):
    name = models.CharField(max_length=250)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='values')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Attribute Values'
        ordering = ['-created']

    def __str__(self):
        return self.name    


class ProductVariation(SoftDeleteModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    opening_qty = models.IntegerField(null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Product Variations'
        ordering = ['-created']

    def __str__(self):
        return self.product.name   


class ProductVariationValue(models.Model):
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='variation_values')     
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE) 
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Variation Values'
        ordering = ['-created']   
        



class HomeSitemap(Sitemap):
    priority = 1.0

    def items(self):
        return [self]

    def location(self, obj: Product) -> str:
        return '/' 
        
    def lastmod(self, obj):
        return datetime.now()

class ProductSitemap(Sitemap):
    priority = 1.0

    def items(self):
        return Product.objects.all()

    def location(self, obj: Product) -> str:
        return '/product/%s' % (obj.slug)   
        
    def lastmod(self, obj):
        return datetime.now() - timedelta(days=5)
        
        
class ProductEnquiry(SoftDeleteModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="enquiries")
    phone = models.CharField(max_length=13, validators=[phone_validator])

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} - {self.phone}'
    

class ProductImageSitemap(Sitemap):
    priority = 0.80

    def items(self):
        return ProductImage.objects.all()

    def location(self, obj: ProductImage) -> str:
        return obj.image.url