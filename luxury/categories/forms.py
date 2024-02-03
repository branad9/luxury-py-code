from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from .models import *


class MainCategoryForm(forms.ModelForm):
    class Meta:
        model = MainCategory
        fields = ('name', 'image','meta_title', 'content', 'active', 'meta_desc', 'meta_keywords', 'robots', 'schema')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-2'),
                Column('image', css_class='form-group col-md-6 mb-2'),
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
            Row(
                Column('meta_title', css_class='form-group col-md-4 mb-2'),
                Column('meta_keywords', css_class='form-group col-md-4 mb-2'),
                Column('robots', css_class='form-group col-md-4 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('meta_desc', css_class='form-group col-md-6 mb-2'),
                Column('schema', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            ),
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'main_category', 'image', 'meta_title', 'meta_desc', 'meta_keywords', 'schema', 'robots', 'content', 'active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-2'),
                Column('main_category', css_class='form-group col-md-4 mb-2'),
                Column('image', css_class='form-group col-md-4 mb-2'),
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
            Row(
                Column('meta_title', css_class='form-group col-md-4 mb-2'),
                Column('meta_keywords', css_class='form-group col-md-4 mb-2'),
                Column('robots', css_class='form-group col-md-4 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('meta_desc', css_class='form-group col-md-6 mb-2'),
                Column('schema', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            ),
        )


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ('name', 'category', 'meta_title', 'meta_desc', 'meta_keywords', 'content', 'active', 'schema', 'robots')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-2'),
                Column('category', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('meta_title', css_class='form-group col-md-4 mb-2'),
                Column('meta_keywords', css_class='form-group col-md-4 mb-2'),
                Column('robots', css_class='form-group col-md-4 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('active', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('content', css_class='form-group col-md-12 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('meta_desc', css_class='form-group col-md-6 mb-2'),
                Column('schema', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            ),
        )


class BrandForm(forms.ModelForm):
    schema = forms.CharField(widget=forms.Textarea(attrs={"rows":"17"}))

    class Meta:
        model = Brand
        fields = ('name', 'category', 'image', 'category_image', 'meta_title', 'meta_desc', 'meta_keywords',  'meta_title2', 'meta_desc2', 'meta_keywords2', 'schema', 'content', 'active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-2'),
                Column('category', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                
                Column('image', css_class='form-group col-md-6 mb-2'),
                Column('category_image', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('meta_title', css_class='form-group col-md-6 mb-2'),
                Column('meta_title2', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('meta_desc', css_class='form-group col-md-6 mb-2'),
                Column('meta_desc2', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('meta_keywords', css_class='form-group col-md-6 mb-2'),
                Column('meta_keywords2', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),           
            Row(
                Column('schema', css_class='form-group col-md-6 mb-2'),
                Column('content', css_class='form-group col-md-6 mb-2'),
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


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', 'active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-6 mb-2'),
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
        
        
class BrandContentForm(forms.ModelForm):
    class Meta:
        model = BrandContent
        fields = ('category', 'brand', 'content')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('category', css_class='form-group col-md-6 mb-2'),
                Column('brand', css_class='form-group col-md-6 mb-2'),
                css_class='form-row'
            ),
            Row(
                Column('content', css_class='form-group col-md-12 mb-2'),
                css_class='form-row'
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='btn btn-primary')
            ),
        )        
        