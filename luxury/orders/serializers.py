from rest_framework import serializers
from .models import *
from products.models import ProductVariationValue
from products.serializers import WebProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'variation', 'qty', 'price')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('user', 'order_number', 'order_note', 'order_total', 'delivery_charges', 'status', 'items')

    def create(self, validated_data):   
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order               


class OrderProductVariationValueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    attribute = serializers.StringRelatedField()
    attribute_value =  serializers.StringRelatedField()

    class Meta:
        model = ProductVariationValue
        fields = ('id', 'attribute', 'attribute_value')  


class OrderProductVariationSerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField('get_values')

    def get_values(self, variation):
        qs = ProductVariationValue.objects.filter(variation=variation)
        serializer = OrderProductVariationValueSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = ProductVariation
        fields = ('id', 'price', 'sale_price', 'opening_qty', 'in_stock', 'values')    

class ReadOrderItemSerializer(serializers.ModelSerializer):
    product = WebProductSerializer()
    variation = OrderProductVariationSerializer()
    class Meta:
        model = OrderItem
        fields = ('product', 'variation', 'qty', 'price')


class ReadOrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('get_items')

    def get_items(self, order):
        qs = OrderItem.objects.filter(order=order)
        serializer = ReadOrderItemSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Order
        fields = ('id', 'user', 'order_number', 'order_note', 'order_total', 'delivery_charges', 'status', 'items', 'track_number', 'created')