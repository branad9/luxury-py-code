from asyncore import read
from rest_framework import serializers
from .models import *
from products.serializers import ProductImageSerializer

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    brand = serializers.StringRelatedField()
    main_category = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    subcategory = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'code', 'main_category', 'category', 'subcategory', 'brand', 'active', 'specs', 'images')


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'
