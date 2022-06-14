from django.db import models
from django.utils import timezone



class Customer(models.Model):
    """docstring for Customer"""
    
    GENDER_CHOICES=(('Masculin','Masculin'),('Féminin','Féminin'),('Autre','Autre')
    )
    
    REGION_CHOICES=(("Auvergne-Rhône-Alpes","Auvergne-Rhône-Alpes"),("Bourgogne-Franche-Comté","Bourgogne-Franche-Comté"),("Bretagne","Bretagne"),("Centre-Val de Loire","Centre-Val de Loire"),("Corse","Corse"),("Grand Est","Grand Est"),("Hauts-de-France","Hauts-de-France"),("IDF","IDF"),("Normandie","Normandie"),("Nouvelle-Aquitaine","Nouvelle-Aquitaine"),("Occitanie","Occitanie"),("Pays de la Loire","Pays de la Loire"),("Provence-Alpes-Côte d’Azur","Provence-Alpes-Côte d’Azur"))
    
    name=models.CharField(max_length=255,blank=True, null=True)
    customer_type=models.CharField(max_length=255,blank=True, null=True)
    dob=models.DateTimeField(blank=True,null=True)
    gender=models.CharField(max_length=255, null=True,choices=GENDER_CHOICES)
    email=models.CharField(max_length=255,blank=True, null=True) 
    phone=models.CharField(max_length=12,blank=True, null=True)
    address=models.TextField(blank=True, null=True)
    town=models.CharField(max_length=255,blank=True, null=True)
    region=models.CharField(max_length=255,blank=True, null=True,choices=REGION_CHOICES)
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
        return round(total,2)
    
    @property
    def segment(self):
        if self.total_orders>100000:
            segmentation="Stars"
        elif self.total_orders==0:
            segmentation="Nouvelle inscription"
        else:
            segmentation="Potentiel moyen"
        return segmentation
    
    @property
    def customer_satisfaction(self):
        my_orders=Order.objects.filter(status="livré",customer__id=self.id)
        total,count=0,0
        if my_orders.count():
            for item in my_orders:
                total=total+item.satisfaction_score
                count=count+1
            return round(total/count,2)
        else:
            return "NA"
    
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
    description=models.TextField(null=True)
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
        quantity_out=self.stock_q
        for order in my_orders:
            quantity_out=quantity_out-order.quantity
        return quantity_out
        
        
    @property
    def stock_status(self):#for particular product order total
        if self.stock_q_actuel < self.stock_security:
            stock_res="A réapprovisionner"
        else:
            stock_res="Okay"
        return stock_res
    
    @property
    def revenues_per_product(self):
        my_orders=Order.objects.filter(product=self)
        revenues=0
        for order in my_orders:
            revenues=revenues+order.get_total_order_price_HT
        return round(revenues,0)
            
    
    
class Order(models.Model):  
    """docstring for Order"""
    
    STATUS_CHOICES=(('en préparation','en préparation'),('expédié','expédié'),('livré','livré'))
    
    customer=models.ForeignKey(Customer,null=True, on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True, on_delete=models.SET_NULL)
    
    date=models.DateTimeField(blank=True, null=True) 
    quantity=models.FloatField(null=True)
    discount=models.FloatField(null=True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    
    status=models.CharField(max_length=255, null=True,default='livré',choices=STATUS_CHOICES)
    Delivery_date_expected=models.DateTimeField(blank=True,null=True)
    Delivery_date_final=models.DateTimeField(blank=True, null=True)
    
    satisfaction_score=models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return "Commande "+ str(self.id)
    
    @property
    def get_total_item_price_HT(self):
        if self.discount=="":
            return round(self.quantity * self.product.price_pdt_HT,2)
        else:
            return round(self.quantity * self.product.price_pdt_HT*((100-self.discount)/100),2)
    
    @property
    def get_total_item_price_TTC(self):
        if self.discount=="":
            return round(self.quantity * self.product.price_pdt_TTC,2)
        else:
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
        if self.get_total_item_price_HT<10000:
            fees_res=100
        else:
            fees_res=0
        return fees_res
    
    @property
    def get_total_order_price_HT(self):#for particular product order total
        TAUX_TVA=1.2
        return self.get_total_item_price_HT+self.delivery_fees/TAUX_TVA
    
    @property
    def get_total_order_price_TTC(self):#for particular product order total
        return self.get_total_item_price_TTC+self.delivery_fees
    
    @property
    def commercial_margin_total(self):
        return round(self.quantity * self.product.price_pdt_HT*(self.product.commercial_margin-(self.discount/100)),2)
    
    
    
class Claim(models.Model):  
    """docstring for Claim"""
    
    TYPE_CHOICES=(('erreur prix','erreur prix'),('article erronné','article erronné'),('article defectueux','article defectueux'),('retard livraison','retard livraison'))
    STATUS_CHOICES=(('ouverte','ouverte'),('résolue','résolue'))
    OPERATOR_CHOICES=(('Amani','Amani'),('Harley','Harley'),('Robin','Robin'))
    
    customer=models.ForeignKey(Customer,null=True, on_delete=models.SET_NULL)
    order=models.ForeignKey(Order,null=True, on_delete=models.SET_NULL)
    date=models.DateTimeField(blank=True,null=True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    description=models.TextField(max_length=255, null=True)
    Operator=models.CharField(max_length=255, null=True,choices=OPERATOR_CHOICES) # A choisir dans users
    Type=models.CharField(max_length=255, null=True,choices=TYPE_CHOICES)
    action=models.TextField(max_length=255, null=True)
    status=models.CharField(max_length=255, null=True,default='ouverte',choices=STATUS_CHOICES)
    
    resolution_date_expected=models.DateTimeField(blank=True,null=True)
    last_contact_customer_date=models.DateTimeField(blank=True, null=True)
    resolution_date_final=models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return "Réclamation " + str(self.id)
    
    def resolution_progress_status(self):
        today=timezone.now()
        if self.resolution_date_final:
            if self.resolution_date_expected < self.resolution_date_final:
                resolution_res="En retard"
            else:
                resolution_res="Dans les temps"
        else:
            if self.resolution_date_expected < today:
                resolution_res="En retard"
            else:
                resolution_res="Dans les temps"
        return resolution_res

class Marketing (models.Model):
    """docstring for Marketing"""
    
    CUSTOMER_SEGMENT_CHOICES=(("Stars","Stars"),("Nouvelle inscription","Nouvelle inscription"),("Potentiel moyen","Potentiel moyen"))
    
    customer_segment=models.CharField(max_length=255, null=True,choices=CUSTOMER_SEGMENT_CHOICES)
    description=models.TextField(max_length=255, null=True)
    start_date=models.DateTimeField(blank=True,null=True)
    end_date=models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return "Campagne Marketing "+ str(self.id)

   
    @property
    def marketing_type(self):
        if self.customer_segment=="Stars":
            mark_type="Invitation_webinaire"
        elif self.customer_segment=="Nouvelle inscription":
            mark_type="Envoi Newsletters"
        else:
            mark_type="Promotions_ciblées"
        return mark_type
            
    

    @property
    def marketing_status(self):
        today=timezone.now()
        if self.end_date < today:
            status_res="Campagne Terminée"
        else:
            status_res="Campagne en cours"
        return status_res
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    