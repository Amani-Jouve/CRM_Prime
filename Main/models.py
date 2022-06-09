from django.db import models
from django.utils import timezone



class Customer(models.Model):
    """docstring fos Customer"""
    
    GENDER_CHOICES=(('Masculin','Masculin'),('Féminin','Féminin'),('Autre','Autre')
    )
    
    name=models.CharField(max_length=255,blank=True, null=True)
    customer_type=models.CharField(max_length=255,blank=True, null=True)
    gender=models.CharField(max_length=255, null=True,choices=GENDER_CHOICES)
    email=models.CharField(max_length=255,blank=True, null=True) 
    phone=models.CharField(max_length=12,blank=True, null=True)
    address=models.CharField(max_length=255,blank=True, null=True)
    town=models.CharField(max_length=255,blank=True, null=True)
    region=models.CharField(max_length=255,blank=True, null=True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name

    @property
    def nb_orders(self):
        my_orders=Order.objects.filter(customer__id=self.id)
        return my_orders.count()
    
    @property
    def total_orders(self):
        my_orders=Order.objects.filter(customer__id=self.id)
        total=0
        for item in my_orders:
            total=total+item.get_total_order_price_TTC
        return total
    
    @property
    def segment(self):
        if self.total_orders>1000:
            segmentation="Bon client"
        else:
            segmentation="Client ponctuel"
        return segmentation

class Product(models.Model):
    """docstring fos Product"""
    
    CATEGORY_CHOICES=(('PC','PC'),('Autre','Autre'))
    
    name=models.CharField(max_length=200, null=True)
    description=models.CharField(max_length=200, null=True)
    category=models.CharField(max_length=200, null=True,choices=CATEGORY_CHOICES)
    n_lot=models.CharField(max_length=200, null=True)
    price_pdt_HT=models.FloatField(null=True)
    price_pdt_TTC=models.FloatField(null=True)
    commercial_margin=models.FloatField(null=True)
    stock_q=models.IntegerField(null=True)
    stock_security=models.IntegerField(null=True)
    
    
    def __str__(self):
        return self.name    
    
    @property
    def stock_q_actuel(self):
        my_orders=Order.objects.filter(product__id=self.id)
        return self.stock_q-my_orders.count()
        
        
    @property
    def stock_status(self):#for particular product order total
        if self.stock_q_actuel < self.stock_security:
            stock_res="A réapprovisionner"
        else:
            stock_res="Okay"
        return stock_res
    
    
    
class Order(models.Model):  
    """docstring fos Order"""
    
    STATUS_CHOICES=(('en préparation','en préparation'),('expédié','expédié'),('livré','livré'),('retour client','retour client'))
    
    
#     name=models.CharField(max_length=200, null=True)
    customer=models.ForeignKey(Customer,null=True, on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True, on_delete=models.SET_NULL)
    
    quantity=models.FloatField(null=True)
    discount=models.FloatField(blank=True,null=True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    
    status=models.CharField(max_length=255, null=True,choices=STATUS_CHOICES)
    Delivery_date_expected=models.DateTimeField(null=True)
    Delivery_date_final=models.DateTimeField(blank=True, null=True)       
    
#     def __str__(self):
#         return self.product.name

    @property
    def get_total_item_price_HT(self):#for particular product order total
        return self.quantity * self.product.price_pdt_HT*(1-self.discount)
    
    @property
    def get_total_item_price_TTC(self):#for particular product order total
        return self.quantity * self.product.price_pdt_TTC*(1-self.discount)
    
    @property
    def late_delivery(self):
        today=timezone.now()
        if self.Delivery_date_expected < today:
            delivery_res="En retard"
        else:
            delivery_res="Dans les temps"
        return delivery_res
    
    @property
    def delivery_fees(self):
        if self.get_total_item_price_HT<2000:
            fees_res=10
        else:
            fees_res=0
        return fees_res
    
    @property
    def get_total_order_price_TTC(self):#for particular product order total
        return self.get_total_item_price_TTC+self.delivery_fees
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    