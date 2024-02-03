from django.db import models
from home.models import SoftDeleteModel
from ckeditor.fields import RichTextField
from django.contrib.sitemaps import Sitemap


class Blog(SoftDeleteModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    date = models.DateField()
    image = models.ImageField(upload_to='images/blogs', null=True, blank=True)
    img_alt = models.CharField(max_length=250)
    meta_desc = models.TextField(max_length=500)
    keywords = models.CharField(max_length=250)
    robots = models.CharField(max_length=250, null=True, blank=True)
    schema = models.TextField(max_length=1000, null=True, blank=True)
    content = RichTextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Blogs'
        ordering = ['-created']

    def __str__(self):
        return self.name


class BlogSitemap(Sitemap):
    priority = 1.0

    def items(self):
        return Blog.objects.all()

    def location(self, obj: Blog) -> str:
        return '/blogs/%s' % (obj.slug)   
        
    def lastmod(self, obj):
        return obj.date
        

class Newsletter(SoftDeleteModel):
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Newsletters'
        ordering = ['-created']

    def __str__(self):
        return self.name        