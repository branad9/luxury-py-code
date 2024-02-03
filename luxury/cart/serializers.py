from rest_framework import serializers
from products.serializers import WebProductSerializer
from products.models import *
from .models import *


class CartProductVariationValueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    attribute = serializers.StringRelatedField()
    attribute_value = serializers.StringRelatedField()

    class Meta:
        model = ProductVariationValue
        fields = ('id', 'attribute', 'attribute_value')  


class CartProductVariationSerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField('get_values')

    def get_values(self, variation):
        qs = ProductVariationValue.objects.filter(variation=variation)
        serializer = CartProductVariationValueSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = ProductVariation
        fields = ('id', 'price', 'sale_price', 'opening_qty', 'in_stock', 'values') 



class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class ReadCartItemSerializer(serializers.ModelSerializer):
    product = WebProductSerializer()
    variation = CartProductVariationSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'user', 'product', 'variation', 'total', 'qty')