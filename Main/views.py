from django.shortcuts import render,redirect
from .models import Customer,Product,Order,Claim, Marketing
from .forms import CustomerForm,ProductForm,OrderForm,ClaimForm,MarketingForm
from datetime import datetime
from .sales_chart import build_comparative_sales_chart

########## Pages / vues principales ##########

def home(request):
    
    my_top_cus=[]
    my_cus = Customer.objects.all()
    
    # Clients CA sup à x K€ #
    for item in my_cus:
        if item.total_orders>150000:
            my_top_cus.append(item)
    
    my_top_pdt=[]
    my_critical_pdt=[]
    my_pdt= Product.objects.all()
    
    # Produits CA sup à y K€ #
    # Stock à réapprovisionner # 
    for machin in my_pdt:
        if machin.revenues_per_product>100000:
            my_top_pdt.append(machin)
        if machin.stock_status=="A réapprovisionner":
            my_critical_pdt.append(machin)
            
    my_ongoing_deliveries=[]
    my_orders=Order.objects.all()
    
    # Commandes en cours de livraison #
    for obj in my_orders:
        if obj.status!="livré":
            my_ongoing_deliveries.append(obj)
    
    my_delayed_claims=[]
    my_claims=Claim.objects.all()
    
    # Réclamations en cours #
    for pb in my_claims:
        if pb.status=="ouverte":
            my_delayed_claims.append(pb)
            
    my_ongoing_marketing=[]
    my_marketing=Marketing.objects.all()
    
    # Campagnes marketing en cours #
    for campaign in my_marketing:
        if campaign.marketing_status=="Campagne en cours":
            my_ongoing_marketing.append(campaign)
            
    # Nbre commandes 2022 & 2021 #
    # CA 2022 & 2021 #
    # Marge commerciale 2022 & 2021 #
    # Satisfaction client globale 2022 & 2021 #
    number_orders_2022,number_orders_2021=0,0
    revenues_2022,revenues_2021=0,0
    com_margin_2022,com_margin_2021=0,0   
    satisfaction_client_globale_2022,satisfaction_client_globale_2021=0,0
    counter_2,counter_1=0,0
    
    for order in my_orders:
        if order.date.strftime("%Y")=="2022":
            number_orders_2022=number_orders_2022+1
            revenues_2022=revenues_2022+order.get_total_item_price_TTC
            com_margin_2022=com_margin_2022+order.commercial_margin_total
            if order.satisfaction_score!=None:
                satisfaction_client_globale_2022=satisfaction_client_globale_2022+order.satisfaction_score
                counter_2=counter_2+1
            
        if order.date.strftime("%Y")=="2021":
            number_orders_2021=number_orders_2021+1
            revenues_2021=revenues_2021+order.get_total_item_price_TTC
            com_margin_2021=com_margin_2021+order.commercial_margin_total
            if order.satisfaction_score!=None:
                satisfaction_client_globale_2021=satisfaction_client_globale_2021+order.satisfaction_score
                counter_1=counter_1+1
    if counter_2:
        satisfaction_client_globale_2022=round(satisfaction_client_globale_2022/counter_2,2)
        
    if counter_1:
        satisfaction_client_globale_2021=round(satisfaction_client_globale_2021/counter_1,2)

            
    # Appel à la fonction d'affichage du graphe - comparatif des sales
    chart_dump = build_comparative_sales_chart()
    
    context = {"customer_top_list" : my_top_cus,"product_top_list" : my_top_pdt,"product_critical_list" : my_critical_pdt,"product_ongoing_deliveries":my_ongoing_deliveries,"alerte_claims":my_delayed_claims,"marketing_en_cours":my_ongoing_marketing,"number_orders_2021":number_orders_2021,"number_orders_2022":number_orders_2022,"revenues_2022":revenues_2022,"revenues_2021":revenues_2021,"com_margin_2022":com_margin_2022,"com_margin_2021":com_margin_2021, "sales_chart": chart_dump,"satisfaction_client_globale_2022":satisfaction_client_globale_2022,"satisfaction_client_globale_2021":satisfaction_client_globale_2021}
  
    return render(request,'Main/home.html', context)

def customers(request):
    my_customer=Customer.objects.order_by('name')
    context={"my_customer": my_customer}
    return render(request,'Main/customers.html',context)

def products(request):
    my_product=Product.objects.order_by('name')
    context={"my_product": my_product}
    return render(request,'Main/products.html',context)

def orders(request):
    my_order=Order.objects.order_by('date_created')
    context={"my_order": my_order}
    return render(request,'Main/orders.html',context)

def claims(request):
    my_claim=Claim.objects.order_by('date_created')
    context={"my_claim": my_claim}
    return render(request,'Main/claims.html',context)

def marketing_campaigns(request):
    my_marketing=Marketing.objects.order_by('start_date')
    context={"my_marketing": my_marketing}
    return render(request,'Main/marketing_campaigns.html',context)

def faq(request):
    return render(request,'Main/faq.html')

########## Pages / vues - Création ##########

def create_customers(request):
    customer_form=CustomerForm()
    context={'form':customer_form}
    if request.method == "POST":
        customer_form=CustomerForm(request.POST)
        if customer_form.is_valid():
            customer_form.save()
            
        return redirect('/Clients/')
    else:
        return render(request,'Main/customers_form.html',context)  

def create_products(request):
    product_form=ProductForm()
    context={'form':product_form}
    if request.method == "POST":
        product_form=ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            
        return redirect('/Produits/')
    else:
        return render(request,'Main/products_form.html',context)

def create_orders(request):
    order_form=OrderForm()
    context={'form':order_form}
#     print(dir(order_form))
    if request.method == "POST":
        order_form=OrderForm(request.POST)
        if order_form.is_valid(): 
            order_date=order_form.cleaned_data.get("date")
            expected_delivery_date=order_form.cleaned_data.get("Delivery_date_expected")
            final_delivery_date=order_form.cleaned_data.get("Delivery_date_final")
            delivery_status=order_form.cleaned_data.get("status")
            product_name_spe=order_form.cleaned_data.get("product")
            product_quantity=order_form.cleaned_data.get("quantity")
            product_spe=Product.objects.get(name=product_name_spe)
            if product_spe.stock_q_actuel>product_quantity:
                if expected_delivery_date>order_date:
                    if delivery_status=="livré":
                        if final_delivery_date!=None:
                            if final_delivery_date>order_date:
                                order_form.save()
                            else:
                                return render(request,'Main/error.html')   
                        else:
                            return render(request,'Main/error.html') 
                    else:
                        order_form.save()
                else:
                    return render(request,'Main/error.html')
            else:
                return render(request,'Main/error.html')             
            
        return redirect('/Commandes/')
    else:
        return render(request,'Main/orders_form.html',context)
    
def create_claims(request):
    claim_form=ClaimForm()
    context={'form':claim_form}
    if request.method == "POST":
        claim_form=ClaimForm(request.POST)
        if claim_form.is_valid():
            claim_form.save()
            
        return redirect('/Réclamations/')
    else:
        return render(request,'Main/claims_form.html',context)

def create_marketing(request):
    marketing_form=MarketingForm()
    context={'form':marketing_form}
    if request.method == "POST":
        marketing_form=MarketingForm(request.POST)
        if marketing_form.is_valid():
            marketing_form.save()
            
        return redirect('/Campagnes_Marketing/')
    else:
        return render(request,'Main/marketing_form.html',context)
    
########## Pages / vues - Update ##########

def update_customer(request,pk):
    my_customer=Customer.objects.get(id=pk)
    if request.method == 'POST':
        my_form=CustomerForm(request.POST,instance=my_customer)
        if my_form.is_valid():
            my_form.save()
            return redirect('/Clients/')
    
    my_form= CustomerForm(instance=my_customer)
    context={'customer':my_customer,'form':my_form}
    return render(request, 'Main/customer_update.html',context)

    
    return render(request,'Main/customers_form.html')

def update_product(request,pk):
    my_product=Product.objects.get(id=pk)
    if request.method == 'POST':
        my_form=ProductForm(request.POST,instance=my_product)
        if my_form.is_valid():
            my_form.save()
            return redirect('/Produits/')
    
    my_form= ProductForm(instance=my_product)
    context={'product':my_product,'form':my_form}
    return render(request, 'Main/product_update.html',context)

def update_order(request,pk):
    my_order=Order.objects.get(id=pk)
    if request.method == 'POST':
        order_form=OrderForm(request.POST,instance=my_order)
        if order_form.is_valid(): 
            order_date=order_form.cleaned_data.get("date")
            expected_delivery_date=order_form.cleaned_data.get("Delivery_date_expected")
            final_delivery_date=order_form.cleaned_data.get("Delivery_date_final")
            delivery_status=order_form.cleaned_data.get("status")
            product_name_spe=order_form.cleaned_data.get("product")
            product_quantity=order_form.cleaned_data.get("quantity")
            product_spe=Product.objects.get(name=product_name_spe)
            if product_spe.stock_q_actuel>product_quantity:
                if expected_delivery_date>order_date:
                    if delivery_status=="livré":
                        if final_delivery_date!=None:
                            if final_delivery_date>order_date:
                                order_form.save()
                            else:
                                return render(request,'Main/error.html')   
                        else:
                            return render(request,'Main/error.html') 
                    else:
                        order_form.save()
                else:
                    return render(request,'Main/error.html')
            else:
                return render(request,'Main/error.html')
            return redirect('/Commandes/')
    
    my_form= OrderForm(instance=my_order)
    context={'order':my_order,'form':my_form}
    return render(request, 'Main/order_update.html',context)

def update_claim(request,pk):
    my_claim=Claim.objects.get(id=pk)
    if request.method == 'POST':
        my_form=ClaimForm(request.POST,instance=my_claim)
        if my_form.is_valid():
            my_form.save()
            return redirect('/Réclamations/')
    
    my_form= ClaimForm(instance=my_claim)
    context={'claim':my_claim,'form':my_form}
    return render(request, 'Main/claim_update.html',context)

def update_marketing(request,pk):
    my_marketing=Marketing.objects.get(id=pk)
    if request.method == 'POST':
        my_form=MarketingForm(request.POST,instance=my_marketing)
        if my_form.is_valid():
            my_form.save()
            return redirect('/Campagnes_Marketing/')
    
    my_form= MarketingForm(instance=my_marketing)
    context={'marketing':my_marketing,'form':my_form}
    return render(request, 'Main/marketing_update.html',context)


########## Pages / vues - Delete ##########

def delete_customer(request,pk):
    item=Customer.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/Clients/')
    context = {'item':item}
    return render(request, 'Main/customer_delete.html', context)

def delete_product(request,pk):
    item=Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/Produits/')
    context = {'item':item}
    return render(request, 'Main/product_delete.html', context)

def delete_order(request,pk):
    item=Order.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/Commandes/')
    context = {'item':item}
    return render(request, 'Main/order_delete.html', context)

def delete_claim(request,pk):
    item=Claim.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/Réclamations/')
    context = {'item':item}
    return render(request, 'Main/claim_delete.html', context)

def delete_marketing(request,pk):
    item=Marketing.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/Campagnes_Marketing/')
    context = {'item':item}
    return render(request, 'Main/marketing_delete.html', context)

