from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from .models import *


class BlogForm(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Blog
        fields = ('name', 'date', 'image', 'img_alt', 'meta_desc', 'keywords', 'content', 'robots', 'schema', 'active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-2'),
                Column('date', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('image', css_class='form-group col-md-6 mb-2'),
                Column('img_alt', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('robots', css_class='form-group col-md-6 mb-2'),
                Column('keywords', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('meta_desc', css_class='form-group col-md-6 mb-2'),
                Column('schema', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('content', css_class='form-group col-md-12 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('active', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            ),
        )
