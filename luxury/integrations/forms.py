from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

from .models import Integration


class IntegrationForm(forms.ModelForm):
    class Meta:
        model = Integration
        fields = ("pages", "head_code", "body_code", "footer_code")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(Column("pages", css_class="form-group col-md-4"), css_class="form-row"),
            Row(
                Column("head_code", css_class="form-group col-md-4"),
                Column("body_code", css_class="form-group col-md-4"),
                Column("footer_code", css_class="form-group col-md-4"),
                css_class="form-row",
            ),
            FormActions(Submit("submit", "Submit", css_class="btn btn-primary")),
        )
