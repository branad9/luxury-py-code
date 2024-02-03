from django import forms
from django_filters import FilterSet, CharFilter, TypedChoiceFilter
from .models import Product
from django.db.models import Q


class ProductFilter(FilterSet):
    TYPE_CHOICES = (
        ('Simple', 'Simple'),
        ('Variable', 'Variable'),
    )
    name = CharFilter(field_name='name', label='Product', lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}))
    code = CharFilter(field_name='code', label='Code', lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}))
    type = TypedChoiceFilter(field_name='type', label='Type', choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Type'}))
    
    class Meta:
        model = Product
        fields = ('name', 'code', 'type')
