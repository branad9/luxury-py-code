from rest_framework import serializers
from categories.serializers import MainCategorySerializer, SubcategorySerializer
from PIL import Image
from io import BytesIO
from django.core.files import File
from rest_framework.validators import UniqueValidator
from django.db.models import Q

from .models import *


def reduce_image_size(image):
    img = Image.open(image)
    thumb_io = BytesIO()
    img.save(thumb_io, 'jpeg', quality=30, optimize=True)
    new_image = File(thumb_io, name=image.name)
    return new_image


class ReadAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'


class AddAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ('name',)


class UpdateAttributeValueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = AttributeValue
        fields = ('id', 'attribute', 'name')
        read_only_fields = ('attribute',)


class ReadAttributeSerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField('get_values')

    def get_values(self, attribute):
        qs = AttributeValue.objects.filter(attribute=attribute)
        serializer = ReadAttributeValueSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Attribute
        fields = ('id', 'name', 'active', 'values')


class AddAttributeSerializer(serializers.ModelSerializer):
    values = AddAttributeValueSerializer(many=True)

    class Meta:
        model = Attribute
        fields = ('name', 'active', 'values')

    def create(self, validated_data):   
        values_data = validated_data.pop('values')
        attribute = Attribute.objects.create(**validated_data)
        for item in values_data:
            AttributeValue.objects.create(attribute=attribute, **item)
        return attribute  


class UpdateAttributeSerializer(serializers.ModelSerializer):
    values = UpdateAttributeValueSerializer(many=True)

    class Meta:
        model = Attribute
        fields = ('name', 'active', 'values')

    def update(self, instance, validated_data):
        values_data = validated_data.pop('values')
        instance.name = validated_data.get('name', instance.name)
        instance.active = validated_data.get('active', instance.active)
        instance.save()

        keep_values = []
        for value in values_data:
            if "id" in value.keys():
                try:
                    v = AttributeValue.objects.get(id=value['id'])
                    v.name = value.get('name', v.name)
                    v.save()
                    keep_values.append(v.id)
                except AttributeValue.DoesNotExist:
                    pass    
            else:
                v = AttributeValue.objects.create(attribute=instance, **value)     
                keep_values.append(v.id)

        for value in instance.values.all():
            if value.id not in keep_values:
                instance.values.filter(id=value.id).delete()     
        return instance     


class ProductImageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[UniqueValidator(queryset=ProductImage.objects.all(), message='An image with this name already exists.')])

    class Meta:
        model = ProductImage
        fields = '__all__'    


class AddProductImageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[UniqueValidator(queryset=ProductImage.objects.all(), message='An image with this name already exists.')])
    
    class Meta:
        model = ProductImage
        fields = ('image', 'name', 'alt', 'default')  


class ReadSimpleProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ('name', 'code', 'main_category', 'category', 'subcategory', 'brand', 'tag', 'price', 'sale_price', 'specs',
                  'desc', 'reference', 'opening_qty', 'in_stock', 'pre_order', 'pre_order_date', 'pre_order_msg', 'length', 
                  'width', 'height', 'type', 'active', 'images', 'meta_title', 'meta_description', 'robots', 'keywords', 'schema')


class AddProductVariationValueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ProductVariationValue
        fields = ('id', 'attribute', 'attribute_value')  


class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = '__all__' 


class ReadProductVariationSerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField('get_values')

    def get_values(self, variation):
        qs = ProductVariationValue.objects.filter(variation=variation)
        serializer = AddProductVariationValueSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = ProductVariation
        fields = ('id', 'price', 'sale_price', 'opening_qty', 'in_stock', 'values')    


class AddProductVariationSerializer(serializers.ModelSerializer):
    values = AddProductVariationValueSerializer(many=True)

    class Meta:
        model = ProductVariation
        fields = ('price', 'sale_price', 'opening_qty', 'in_stock', 'values')  


class UpdateProductVariationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    values = AddProductVariationValueSerializer(many=True)

    class Meta:
        model = ProductVariation
        fields = ('id', 'product', 'price', 'sale_price', 'opening_qty', 'in_stock', 'values')
        read_only_fields = ('product',)


class ReadVariableProductSerializer(serializers.ModelSerializer):
    variations = serializers.SerializerMethodField('get_variations')

    def get_variations(self, product):
        qs = ProductVariation.objects.filter(product=product)
        serializer = ReadProductVariationSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Product
        fields = ('id', 'name', 'code', 'main_category', 'category', 'subcategory', 'brand', 'tag', 'price', 'sale_price', 'desc', 
                  'reference', 'opening_qty', 'in_stock', 'pre_order', 'pre_order_date', 'pre_order_msg', 'length', 'width', 
                  'height', 'type', 'specs', 'active', 'variations')         


class AddSimpleProductSerializer(serializers.ModelSerializer):
    images = AddProductImageSerializer(many=True)                                

    class Meta:
        model = Product
        fields = ('name', 'code', 'main_category', 'category', 'subcategory', 'brand', 'tag', 'price', 'sale_price', 'desc',
                  'reference', 'opening_qty', 'in_stock', 'pre_order', 'pre_order_date', 'pre_order_msg', 'length', 'width', 
                  'height', 'type', 'specs', 'active', 'images', 'meta_title', 'meta_description', 'robots', 'keywords', 'schema')

    def create(self, validated_data):   
        images_data = validated_data.pop('images')
        product = Product.objects.create(**validated_data)
        for item in images_data:
            item['cmp_image'] = reduce_image_size(item['image'])
            ProductImage.objects.create(product=product, **item)
        return product                


class UpdateSimpleProductSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Product
        fields = ('name', 'main_category', 'category', 'subcategory', 'brand', 'tag', 'price', 'sale_price', 'desc', 
                  'reference', 'opening_qty', 'in_stock', 'pre_order', 'pre_order_date', 'pre_order_msg', 'length', 
                  'width', 'height', 'type', 'specs', 'active', 'meta_title', 'meta_description', 'robots', 'keywords', 'schema')  
                  
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.main_category = validated_data.get('main_category', instance.main_category)
        instance.category = validated_data.get('category', instance.category)
        instance.subcategory = validated_data.get('subcategory', instance.subcategory)
        instance.brand = validated_data.get('brand', instance.brand)
        tags = validated_data.get('tag', instance.tag)
        for t in tags:
            instance.tag.add(t)
        instance.price = validated_data.get('price', instance.price)
        instance.sale_price = validated_data.get('sale_price', instance.sale_price)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.reference = validated_data.get('reference', instance.reference)
        instance.opening_qty = validated_data.get('opening_qty', instance.opening_qty)
        instance.in_stock = validated_data.get('in_stock', instance.in_stock)
        instance.pre_order = validated_data.get('pre_order', instance.pre_order)
        instance.pre_order_date = validated_data.get('pre_order_date', instance.pre_order_date)
        instance.pre_order_msg = validated_data.get('pre_order_msg', instance.pre_order_msg)
        instance.length = validated_data.get('length', instance.length)
        instance.width = validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.type = validated_data.get('type', instance.type)
        instance.specs = validated_data.get('specs', instance.specs)
        instance.active = validated_data.get('active', instance.active)
        instance.meta_title = validated_data.get('meta_title', instance.meta_title)
        instance.meta_description = validated_data.get('meta_description', instance.meta_description)
        instance.robots = validated_data.get('robots', instance.robots)
        instance.keywords = validated_data.get('keywords', instance.keywords)
        instance.schema = validated_data.get('schema', instance.schema)
        instance.save()
  
        return instance                  


class AddVariableProductSerializer(serializers.ModelSerializer):
    variations = UpdateProductVariationSerializer(many=True) 

    class Meta:
        model = Product
        fields = ('name', 'code', 'main_category', 'category', 'subcategory', 'brand', 'tag', 'desc', 'reference', 'in_stock', 
                'pre_order', 'pre_order_date', 'pre_order_msg', 'length', 'width', 'height', 'type', 'specs', 'active', 'images', 'variations',
                'meta_title', 'meta_description', 'robots', 'keywords', 'schema')


    def create(self, validated_data):   
        variations_data = validated_data.pop('variations')
        # print(f'variations data {variations_data}')    
        images_data = validated_data.pop('images')
        product = Product.objects.create(**validated_data)
        for item in images_data:
            item['cmp_image'] = reduce_image_size(item['image'])
            ProductImage.objects.create(product=product, **item)
        for item in variations_data:
            values = item.pop('values')
            variant = ProductVariation.objects.create(product=product, **item)
            for v in values:
                # print(f'variation value {v}')
                ProductVariationValue.objects.create(variation=variant, **v)
        return product  


class UpdateVariableProductSerializer(serializers.ModelSerializer):
    variations = UpdateProductVariationSerializer(many=True)  

    class Meta:
        model = Product
        fields = ('name', 'main_category', 'category', 'subcategory', 'brand', 'tag', 'desc', 'reference', 'images',
                  'pre_order', 'pre_order_date', 'pre_order_msg', 'in_stock', 'length', 'width', 'height', 'type', 'specs', 'active', 'variations',
                  'meta_title', 'meta_description', 'robots', 'keywords', 'schema')

    def update(self, instance, validated_data):
        variations_data = validated_data.pop('variations')
        # print(f'variations data {variations_data}')    
        instance.name = validated_data.get('name', instance.name)
        instance.main_category = validated_data.get('main_category', instance.main_category)
        instance.category = validated_data.get('category', instance.category)
        instance.subcategory = validated_data.get('subcategory', instance.subcategory)
        instance.brand = validated_data.get('brand', instance.brand)
        tags = validated_data.get('tag', instance.tag)
        for t in tags:
            instance.tag.add(t)
        instance.price = validated_data.get('price', instance.price)
        instance.sale_price = validated_data.get('sale_price', instance.sale_price)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.reference = validated_data.get('reference', instance.reference)
        instance.opening_qty = validated_data.get('opening_qty', instance.opening_qty)
        instance.in_stock = validated_data.get('in_stock', instance.in_stock)
        instance.pre_order = validated_data.get('pre_order', instance.pre_order)
        instance.pre_order_date = validated_data.get('pre_order_date', instance.pre_order_date)
        instance.pre_order_msg = validated_data.get('pre_order_msg', instance.pre_order_msg)
        instance.length = validated_data.get('length', instance.length)
        instance.width = validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.type = validated_data.get('type', instance.type)
        instance.specs = validated_data.get('specs', instance.specs)
        instance.active = validated_data.get('active', instance.active)
        instance.meta_title = validated_data.get('meta_title', instance.meta_title)
        instance.meta_description = validated_data.get('meta_description', instance.meta_description)
        instance.robots = validated_data.get('robots', instance.robots)
        instance.keywords = validated_data.get('keywords', instance.keywords)
        instance.schema = validated_data.get('schema', instance.schema)
        instance.save()

        keep_variations = []
        for item in variations_data:
            values = item.pop('values')
            if "id" in item.keys():
                try:
                    variant = ProductVariation.objects.get(id=item['id'])
                    variant.price = item.get('price', variant.price)
                    variant.sale_price = item.get('sale_price', variant.sale_price)
                    variant.opening_qty = item.get('opening_qty', variant.opening_qty)
                    variant.in_stock = item.get('in_stock', variant.in_stock)
                    variant.save()
                    variant.variation_values.all().delete()
                    for v in values:
                        ProductVariationValue.objects.create(variation=variant, **v)  
                    keep_variations.append(variant.id)
                except ProductVariation.DoesNotExist:
                    pass    
            else:
                variant = ProductVariation.objects.create(product=instance, **item)
                variant.variation_values.all().delete()  
                for v in values:
                    ProductVariationValue.objects.create(variation=variant, **v)   
                keep_variations.append(variant.id)

        for var in instance.variations.all():
            if var.id not in keep_variations:
                instance.variations.filter(id=var.id).delete()  
              
        return instance  


class WebProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    brand = serializers.StringRelatedField()
    variations = ReadProductVariationSerializer(many=True)
    main_category = MainCategorySerializer()
    category = serializers.StringRelatedField()
    subcategory = SubcategorySerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'code', 'main_category', 'category', 'subcategory', 'brand', 'tag', 'price', 'sale_price', 
                  'desc', 'reference', 'opening_qty', 'in_stock', 'pre_order', 'pre_order_date', 'pre_order_msg', 'length', 'width', 
                  'height', 'type', 'active', 'specs', 'images', 'variations')


class ProductEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductEnquiry
        fields = ('id', 'product', 'phone')