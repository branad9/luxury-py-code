from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from .models import *


class AttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ('name', 'active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-2'),
                Column('active', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            ),
        )


class AttributeValueForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        fields = ('name', 'attribute')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-2'),
                Column('attribute', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            ),
        )


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('image', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            ),
        )
        