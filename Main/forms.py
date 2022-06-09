from django.forms import ModelForm
from .models import Customer
class CustomerForm(ModelForm):
    """docstring for CustomerForm"""
    class Meta():
        model = Customer
        fields = '__all__'