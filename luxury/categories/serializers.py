from rest_framework import serializers
from .models import *


# class CategorySerializer(serializers.ModelSerializer):
#     subcategs = serializers.SerializerMethodField('sub_categs')

#     def sub_categs(self, obj):
#         qs = obj.get_subcategories()
#         serializer = CategorySerializer(instance=qs, many=True)
#         return serializer.data

#     class Meta:
#         model = Category
#         fields = ('id', 'name', 'parent', 'active', 'subcategs')


class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


        