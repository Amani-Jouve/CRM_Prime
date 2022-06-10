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
from .views import home, customers,products,orders,create_customers,create_products,create_orders,update_customer,delete_customer,update_product,delete_product,update_order,delete_order,claims,create_claims,update_claim,delete_claim,marketing_campaigns,create_marketing,update_marketing,delete_marketing

urlpatterns = [
    path('', home, name='home'),
    path('Clients/', customers, name='customers_page'),
    path('Produits/', products, name='products_page'),
    path('Commandes/', orders, name='orders_page'),
    path('Réclamations/', claims, name='claims_page'),
    path('Campagnes_Marketing/',marketing_campaigns, name='marketing_page'),
    
    path('Clients_création/', create_customers, name='customers_create'),
    path('Produits_création/', create_products, name='products_create'),
    path('Commandes_création/', create_orders, name='orders_create'),
    path('Réclamations_création/', create_claims, name='claims_create'),
    path('Campagnes_Marketing_création/', create_marketing, name='marketing_campaigns_create'),
    
    path('Clients_mise_à_jour/<str:pk>',update_customer,name='update_customer'),
    path('Clients_supprimer/<str:pk>',delete_customer,name='delete_customer'),
    
    path('Produits_mise_à_jour/<str:pk>',update_product,name='update_product'),
    path('Produits_supprimer/<str:pk>',delete_product,name='delete_product'),
    
    path('Commandes_mise_à_jour/<str:pk>',update_order,name='update_order'),
    path('Commandes_supprimer/<str:pk>',delete_order,name='delete_order'),

    path('Réclamations_mise_à_jour/<str:pk>',update_claim,name='update_claim'),
    path('Réclamations_supprimer/<str:pk>',delete_claim,name='delete_claim'),
    
    path('Campagne_Marketing_mise_à_jour/<str:pk>',update_marketing,name='update_marketing'),
    path('Campagne_Marketing_supprimer/<str:pk>',delete_marketing,name='delete_marketing'),
]













