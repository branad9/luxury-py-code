from django.db import models
from home.models import SoftDeleteModel
from ckeditor.fields import RichTextField
from django.contrib.sitemaps import Sitemap


class MainCategory(SoftDeleteModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    image = models.ImageField(upload_to='images/maincategories', null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    meta_desc = models.TextField(null=True, blank=True)
    meta_keywords = models.CharField(max_length=250, null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    schema = models.TextField(null=True, blank=True)
    robots = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'MainCategories'
        ordering = ['-created']

    def __str__(self):
        return self.name


class Category(SoftDeleteModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    main_category = models.ForeignKey(MainCategory, on_delete=models.SET_NULL, null=True, related_name='categories')
    image = models.ImageField(upload_to='images/categories', null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    meta_desc = models.TextField(null=True, blank=True)
    meta_keywords = models.CharField(max_length=250, null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    schema = models.TextField(null=True, blank=True)
    robots = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-created']

    def __str__(self):
        return f'{self.name} - {self.main_category}'


class Subcategory(SoftDeleteModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='subcategories')
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    meta_desc = models.TextField(null=True, blank=True)
    meta_keywords = models.CharField(max_length=250, null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    schema = models.TextField(null=True, blank=True)
    robots = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Subcategories'
        ordering = ['-created']

    def __str__(self):
        return self.name


class Brand(SoftDeleteModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='images/brands', null=True, blank=True)
    category_image = models.ImageField(upload_to='images/cbrands', null=True, blank=True)
    meta_title = models.CharField(max_length=250, null=True, blank=True)
    meta_desc = models.CharField(max_length=250, null=True, blank=True)
    meta_keywords = models.CharField(max_length=250, null=True, blank=True)
    meta_title2 = models.CharField(max_length=250, null=True, blank=True)
    meta_desc2 = models.CharField(max_length=250, null=True, blank=True)
    meta_keywords2 = models.CharField(max_length=250, null=True, blank=True)
    schema = models.TextField(null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Brands'
        ordering = ['-created']

    def __str__(self):
        return self.name


class Tag(SoftDeleteModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Tags'
        ordering = ['-created']

    def __str__(self):
        return self.name


class BrandContent(SoftDeleteModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    content = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'BrandContents'
        ordering = ['-created']



class CategorySitemap(Sitemap):
    priority = 1.0

    def items(self):
        return Category.objects.filter(active=True, main_category__active=True)

    def location(self, obj: Category) -> str:
        return f'/{obj.main_category.slug}/{obj.slug}' 
        
    def lastmod(self, obj):
        return obj.updated
        


class SubcategorySitemap(Sitemap):
    priority = 1.0

    def items(self):
        return Subcategory.objects.filter(active=True, category__active=True, category__main_category__active=True)

    def location(self, obj: Subcategory) -> str:
        return f"/{obj.category.main_category.slug}/{obj.category.slug}/{obj.slug}"   
        
    def lastmod(self, obj):
        return obj.updated
        

    