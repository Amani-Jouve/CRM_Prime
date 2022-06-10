from django.shortcuts import render,redirect
from .models import Customer,Product,Order,Claim
from .forms import CustomerForm,ProductForm,OrderForm,ClaimForm

# Pages / vues principales 

def home(request):
    return render(request,'Main/home.html')

def customers(request):
    my_customer=Customer.objects.all()
    context={"my_customer": my_customer}
    return render(request,'Main/customers.html',context)

def products(request):
    my_product=Product.objects.all()
    context={"my_product": my_product}
    return render(request,'Main/products.html',context)

def orders(request):
    my_order=Order.objects.all()
    context={"my_order": my_order}
    return render(request,'Main/orders.html',context)

def claims(request):
    my_claim=Claim.objects.all()
    context={"my_claim": my_claim}
    return render(request,'Main/claims.html',context)

# Pages / vues - Création

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
    if request.method == "POST":
        order_form=OrderForm(request.POST)
        if order_form.is_valid():
            order_form.save()
            
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

# Pages / vues - Update

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
        my_form=OrderForm(request.POST,instance=my_order)
        if my_form.is_valid():
            my_form.save()
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

# Pages / vues - Delete

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