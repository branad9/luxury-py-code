from django import forms
from django_filters import FilterSet, CharFilter
from .models import MainCategory, Category, Subcategory


class MainCategoryFilter(FilterSet):
    name = CharFilter(field_name='name', label='Name', lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    
    class Meta:
        model = MainCategory
        fields = ('name',)


class CategoryFilter(FilterSet):
    name = CharFilter(field_name='name', label='Name', lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    
    class Meta:
        model = Category
        fields = ('name',)


class SubcategoryFilter(FilterSet):
    name = CharFilter(field_name='name', label='Name', lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    
    class Meta:
        model = Subcategory
        fields = ('name',)
