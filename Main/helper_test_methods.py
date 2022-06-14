from django.utils import timezone
from .models import Customer, Product, Order
from datetime import datetime

# TO DO: import choices from models

def helper_create_customer():
	new_customer = Customer()
	new_customer.name = "Yan Solo"
	new_customer.customer_type="Particulier"
	# new_customer.dob = timezone.make_aware(datetime(1977, 7, 1, 0, 0, 0))
	new_customer.gender = "Masculin"
	new_customer.email = "yansolo@gmail.com"
	new_customer.phone = "0678295432"
	new_customer.address = "12 avenue Henri-Martin"
	new_customer.town = "Paris"
	new_customer.region = "IDF"
	return new_customer

def helper_create_product():
	""" Creates a sample product object """
	new_product = Product()
	new_product.name = "PC Dell 1"
	new_product.description = "Un premier PC Dell"
	new_product.category = "Informatique"
	new_product.n_lot = "123456"
	new_product.price_pdt_HT = 1299.99
	new_product.commercial_margin = 200.0
	new_product.stock_q = 10000
	new_product.stock_security = 5

	return new_product

def helper_create_order(customer, product):
	""" Creates a sample order object """
	DEV_DELAY = 2
	new_order = Order()
	# new_order.date = get_timezone_aware_now()
	new_order.customer = Customer.objects.get(id=customer.id)
	new_order.product = Product.objects.get(id=customer.id)

	# date_now = timezone.make_aware(datetime.now())
	# del_date_expected = date_now.replace(day=date_now.day + DEV_DELAY, minute=0, second=0, microsecond=0)

	# new_order.date = date_now
	new_order.quantity = 1
	new_order.discount = 5
	# new_order.date_created = date_now
	new_order.status = "en préparation"
	# new_order.Delivery_date_expected = del_date_expected
	new_order.satisfaction_score = 4.0

	return new_order

def helper_create_claim(self, customer, product):
	""" Creates a sample claim object """
	RES_DELAY = 3
	# date_now = self.get_timezone_aware_now()
	# res_date_expected = date_now.replace(day=date_now.day + RES_DELAY)

	new_claim = Claim()
	new_claim.customer = Customer.objects.get(id=customer.id)
	new_claim.order = Order.objects.get(id=product.id)
	# new_claim.date = date_now
	# new_claim.date_created = date_now
	new_claim.description = "Une première réclamation"
	new_claim.Operator = "Amani"
	new_claim.Type = "article erronné"
	new_claim.action = "Changer l'article"
	new_claim.status = "ouverte"
	# new_claim.resolution_date_expected = res_date_expected

	return new_claim

def helper_create_marketing(self):
	""" Creates a sample marketing object """
	CAMPAIGN_DURATION=1
	# date_now = self.get_timezone_aware_now()
	# end_date = date_now.replace(month=date_now.month + CAMPAIGN_DURATION)

	new_marketing = Marketing()
	new_marketing.customer_segment = "Potentiel moyen"
	new_marketing.description = "Une nouvelle campagne de marketing"
	# new_marketing.start_date = date_now
	# new_marketing.end_date = end_date

	return new_marketing

# def get_timezone_aware_now():
# 	return timezone.make_aware(datetime.now())