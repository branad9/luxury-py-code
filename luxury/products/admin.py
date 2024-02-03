from django.contrib import admin
from .models import *


class AttributeValueInline(admin.StackedInline):
    model = AttributeValue
    extra = 2


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'active')
    inlines = [AttributeValueInline]


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'price', 'sale_price')


@admin.register(ProductVariationValue)
class ProductVariationValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'variation', 'attribute', 'attribute_value')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image')

admin.site.register(Attribute, AttributeAdmin)

admin.site.register(ProductEnquiry)


