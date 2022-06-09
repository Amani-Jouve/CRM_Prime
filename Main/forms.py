from django import forms
from django.forms import ModelForm
from .models import Customer,Product,Order
class CustomerForm(ModelForm):
    """docstring for CustomerForm"""
    class Meta():
        model = Customer
        fields='__all__'
        
class ProductForm(ModelForm):
    """docstring for ProductForm"""
    class Meta():
        model = Product
        fields='__all__'
        
class OrderForm(ModelForm):
    """docstring for OrderForm"""
    class Meta():
        model = Order
        fields='__all__'
        