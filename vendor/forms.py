from django import forms
from product.models import Product
from multiupload.fields import MultiFileField

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'vendor', 'title', 'description', 'price']

class ProductImageForm(forms.Form):
    images = MultiFileField(min_num=1, max_num=5, required=True)
