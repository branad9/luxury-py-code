from django import forms
from django_filters import FilterSet, CharFilter, TypedChoiceFilter
from .models import User


class UserFilter(FilterSet):
    STATUS_CHOICES = (
        (True, 'Active'), 
        (False, 'Inactive'),
    )
    full_name = CharFilter(field_name='full_name', label='Product', lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User name'}))
    email = CharFilter(field_name='email', label='Email', lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone = CharFilter(field_name='phone', label='Phone', lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}))
    is_active = TypedChoiceFilter(field_name='is_active', label='Status', choices=STATUS_CHOICES, widget=forms.Select(attrs={'class':'form-control','placeholder':'Status'}))
    
    class Meta:
        model = User
        fields = ('full_name', 'email', 'phone', 'is_active')
