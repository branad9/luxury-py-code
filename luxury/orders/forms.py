from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from .models import *


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("status", "track_number", "order_note", "cancellation_reason")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("status", css_class="form-group col-md-6 mb-2"),
                Column("track_number", css_class="form-group col-md-6 mb-2"),
                css_class="form-row",
            ),
            Row(
                Column("order_note", css_class="form-group col-md-6 mb-2"),
                Column("cancellation_reason", css_class="form-group col-md-6 mb-2"),
                css_class="form-row",
            ),
            FormActions(Submit("submit", "Submit", css_class="btn btn-primary")),
        )
