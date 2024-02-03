from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

class RobotsForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('content', css_class='form-group col-md-12'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Save', css_class='btn btn-primary')
            ),
        )