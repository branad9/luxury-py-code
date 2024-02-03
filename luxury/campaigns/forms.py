from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from .models import *


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ('title', 'subtitle', 'background_image', 'image_left', 'image_right', 'active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-2'),
                Column('subtitle', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('background_image', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('image_left', css_class='form-group col-md-6 mb-2'),
                Column('image_right', css_class='form-group col-md-6 mb-2'),
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