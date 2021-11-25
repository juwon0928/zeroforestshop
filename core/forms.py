from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from django.forms import ModelForm

from .models import *

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
   

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '쿠폰코드',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))

class PaymentForm(forms.Form):
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)

from django.forms import ModelForm

from .models import *


from django import forms
from .models import Board

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = '__all__'

class CreateForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content', 'writer']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 20}),
            'writer': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'subject': '제목',
            'content': '내용',
            'writer': '작성자',
        }