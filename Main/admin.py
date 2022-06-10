from django.contrib import admin
from .models import Customer,Product,Order,Claim,Marketing

admin.site.register(Customer)

admin.site.register(Product)

admin.site.register(Order)

admin.site.register(Claim)

admin.site.register(Marketing)
