from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from .models import *


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))    

    class Meta:
        model = User
        fields = ('full_name', 'phone', 'email', 'is_superadmin', 'is_active')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('passwords does not match')    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='form-group col-md-6 mb-2'),
                Column('phone', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-8 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('password', css_class='form-group col-md-6 mb-2'),
                Column('confirm_password', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('is_superadmin', css_class='form-group col-md-3 mb-2'),
                Column('is_active', css_class='form-group col-md-3 mb-2'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            ),
        )


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name', 'phone', 'email', 'is_superadmin', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='form-group col-md-6 mb-2'),
                Column('phone', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-8 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('is_superadmin', css_class='form-group col-md-3 mb-2'),
                Column('is_active', css_class='form-group col-md-3 mb-2'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            ),
        )
        

class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name', 'phone', 'email', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='form-group col-md-6 mb-2'),
                Column('phone', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-8 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('is_active', css_class='form-group col-md-3 mb-2'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            ),
        )        


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['full_name', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}),
        }

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('password does not match')
