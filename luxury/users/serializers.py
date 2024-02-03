from rest_framework import serializers
from products.serializers import WebProductSerializer
from products.models import *
from .models import *


class WishlistProductVariationValueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    attribute = serializers.StringRelatedField()
    attribute_value = serializers.StringRelatedField()

    class Meta:
        model = ProductVariationValue
        fields = ('id', 'attribute', 'attribute_value')  


class WishlistProductVariationSerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField('get_values')

    def get_values(self, variation):
        qs = ProductVariationValue.objects.filter(variation=variation)
        serializer = WishlistProductVariationValueSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = ProductVariation
        fields = ('id', 'price', 'sale_price', 'opening_qty', 'in_stock', 'values') 



class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'


class ReadWishlistSerializer(serializers.ModelSerializer):
    product = WebProductSerializer()
    variation = WishlistProductVariationSerializer()

    class Meta:
        model = Wishlist
        fields = ('id', 'user', 'product', 'variation')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
 
        
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        