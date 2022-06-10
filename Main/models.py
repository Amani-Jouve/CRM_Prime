from django.db import models
from django.utils import timezone



class Customer(models.Model):
    """docstring for Customer"""
    
    GENDER_CHOICES=(('Masculin','Masculin'),('Féminin','Féminin'),('Autre','Autre')
    )
    
#     REGION_CHOICES=
    
    name=models.CharField(max_length=255,blank=True, null=True)
    customer_type=models.CharField(max_length=255,blank=True, null=True)
    dob=models.DateTimeField(null=True)
    gender=models.CharField(max_length=255, null=True,choices=GENDER_CHOICES)
    email=models.CharField(max_length=255,blank=True, null=True) 
    phone=models.CharField(max_length=12,blank=True, null=True)
    address=models.CharField(max_length=255,blank=True, null=True)
    town=models.CharField(max_length=255,blank=True, null=True)
    region=models.CharField(max_length=255,blank=True, null=True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)
#     marketing_campaign=models.ForeignKey(Marketing,null=True, on_delete=models.SET_NULL)
    
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
        elif self.total_orders==0:
            segmentation="Nouvelle inscription"
        else:
            segmentation="Client ponctuel"
        return segmentation
    
    @property
    def nb_claims(self):
        my_claims=Claim.objects.filter(customer__id=self.id)
        return my_claims.count()
    
    @property
    def current_marketing_type(self):
        my_marketing=Marketing.objects.get(customer_segment=self.segment)
        if my_marketing.marketing_status=="Campagne en cours":
            return my_marketing.marketing_type
        else:
            return "NA"

class Product(models.Model):
    """docstring for Product"""
    
    CATEGORY_CHOICES=(('Informatique','Informatique'),('Téléphonie','Téléphonie'),('Objets connectés','Objets connectés'),('TV & Home cinéma','TV & Home cinéma'))
    
    name=models.CharField(max_length=200, null=True)
    description=models.CharField(max_length=200, null=True)
    category=models.CharField(max_length=200, null=True,choices=CATEGORY_CHOICES)
    n_lot=models.CharField(max_length=200, null=True)
    price_pdt_HT=models.FloatField(null=True)
    commercial_margin=models.FloatField(null=True)
    stock_q=models.IntegerField(null=True)
    stock_security=models.IntegerField(null=True)
    
    def __str__(self):
        return self.name    
    
    @property
    def price_pdt_TTC(self):
        TAUX_TVA=1.2
        return self.price_pdt_HT*TAUX_TVA
    
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
    """docstring for Order"""
    
    STATUS_CHOICES=(('en préparation','en préparation'),('expédié','expédié'),('livré','livré'),('retour client','retour client'))
    
    customer=models.ForeignKey(Customer,null=True, on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True, on_delete=models.SET_NULL)
    
    quantity=models.FloatField(null=True)
    discount=models.FloatField(blank=True,null=True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    
    status=models.CharField(max_length=255, null=True,default='en préparation',choices=STATUS_CHOICES)
    Delivery_date_expected=models.DateTimeField(null=True)
    Delivery_date_final=models.DateTimeField(blank=True, null=True)       
    
    def __str__(self):
        return "Commande "+ str(self.id)
    
    @property
    def get_total_item_price_HT(self):
        return round(self.quantity * self.product.price_pdt_HT*((100-self.discount)/100),2)
    
    @property
    def get_total_item_price_TTC(self):
        return round(self.quantity * self.product.price_pdt_TTC*((100-self.discount)/100),2)
    
    @property                      # Axe de réfacto
    def late_delivery(self):
        today=timezone.now()
        if self.Delivery_date_final:
            if self.Delivery_date_expected < self.Delivery_date_final:
                delivery_res="En retard"
            else:
                delivery_res="Dans les temps"
        else:
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
    
    
    
class Claim(models.Model):  
    """docstring for Claim"""
    
    TYPE_CHOICES=(('erreur prix','erreur prix'),('article erronné','article erronné'),('article defectueux','article defectueux'),('retard livraison','retard livraison'))
    STATUS_CHOICES=(('ouverte','ouverte'),('résolue','résolue'))
    
    customer=models.ForeignKey(Customer,null=True, on_delete=models.SET_NULL)
    order=models.ForeignKey(Order,null=True, on_delete=models.SET_NULL)
    
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    description=models.CharField(max_length=255, null=True)
    Operator=models.CharField(max_length=255, null=True) # A choisir dans users
    Type=models.CharField(max_length=255, null=True,choices=TYPE_CHOICES)
    action=models.CharField(max_length=255, null=True)
    status=models.CharField(max_length=255, null=True,default='ouverte',choices=STATUS_CHOICES)
    
    resolution_date_expected=models.DateTimeField(null=True)
    last_contact_customer_date=models.DateTimeField(blank=True, null=True)
    resolution_date_final=models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return "Réclamation " + str(self.id)
    
    def resolution_progress_status(self):
        today=timezone.now()
        if self.resolution_date_expected < today:
            resolution_res="En retard"
        else:
            resolution_res="Dans les temps"
        return resolution_res
    
class Marketing (models.Model):
    """docstring for Marketing"""
    
    CUSTOMER_SEGMENT_CHOICES=(("Bon client","Bon client"),("Nouvelle inscription","Nouvelle inscription"),("Client ponctuel","Client ponctuel"))
    
    customer_segment=models.CharField(max_length=255, null=True,choices=CUSTOMER_SEGMENT_CHOICES)
    description=models.CharField(max_length=255, null=True)
    start_date=models.DateTimeField(null=True)
    end_date=models.DateTimeField(null=True)
    
    def __str__(self):
        return "Campagne Marketing "+ str(self.id)

   
    @property
    def marketing_type(self):
        if self.customer_segment=="Bon client":
            mark_type="Listing_promotions_ciblées"
        elif self.customer_segment=="Nouvelle inscription":
            mark_type="Envoi Newsletters"
        else:
            mark_type="Invitation_webinaire"
        return mark_type
            
    

    @property
    def marketing_status(self):
        today=timezone.now()
        if self.end_date < today:
            status_res="Campagne Terminée"
        else:
            status_res="Campagne en cours"
        return status_res
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    