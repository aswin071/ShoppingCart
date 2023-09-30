# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Product


class CreateUserForm(UserCreationForm):

    class Meta:
        model=User
        fields =['username','email','password1','password2']



class ProductForm(forms.ModelForm):
    class Meta:
         model = Product
         fields = ['product_name', 'description', 'price', 'image',]
        
    def __init__(self, *args, **kwargs):
        super(ProductForm,self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['min'] = 0
       

        for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'