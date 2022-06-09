# """Main app URL Configuration

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/3.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """



from django.urls import path
from .views import home, customers,products,orders,create_customers,create_products,create_orders,update_customer,delete_customer,update_product,delete_product

urlpatterns = [
    path('', home, name='home'),
    path('Clients/', customers, name='customers_page'),
    path('Produits/', products, name='products_page'),
    path('Commandes/', orders, name='orders_page'),
    
    path('Clients_création/', create_customers, name='customers_create'),
    path('Produits_création/', create_products, name='products_create'),
    path('Commandes_création/', create_orders, name='orders_create'),
    
    path('Clients_mise_à_jour/<str:pk>',update_customer,name='update_customer'),
    path('Clients_supprimer/<str:pk>',delete_customer,name='delete_customer'),
    
    path('Produits_mise_à_jour/<str:pk>',update_product,name='update_product'),
    path('Produits_supprimer/<str:pk>',delete_product,name='delete_product'),
    
    # Il manque les updates des trois items 
    
]













