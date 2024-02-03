from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from .models import *


class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ('marquee', 'address', 'phone', 'email', 'whatsapp_phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-6 mb-2'),
                Column('phone', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('marquee', css_class='form-group col-md-12 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('address', css_class='form-group col-md-6 mb-2'),
                Column('whatsapp_phone', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            ),
        )
