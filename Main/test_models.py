from django.test import TestCase
from django.http import HttpRequest
from django.db import models
from .models import Customer, Product, Order, Claim, Marketing
from datetime import datetime

class ModelsTest(TestCase):
    def setUp(self):
        self.customer = self.helper_create_customer()
        self.customer.save()

        self.product = self.helper_create_product()
        self.product.save()

        self.order = Order()
        self.claim = Claim()
        self.marketing = Marketing()

    def tearDown(self):
        pass

    def test_can_create_customer_in_database(self):
        self.customer.save()
        self.assertEqual(Customer.objects.first(), self.customer)

    def test_can_create_product_in_database(self):
        self.product.save()
        self.assertEqual(Product.objects.first(), self.product)

    def test_can_create_order_in_database(self):
        self.helper_save_order_in_database()
        self.assertEqual(Order.objects.first(), self.order)

    def test_can_create_claim_in_database(self):
        self.claim.customer = Customer.objects.get(id=self.customer.id)
        self.helper_save_order_in_database()

        self.claim.customer = Customer.objects.get(id=self.customer.id)
        self.claim.order = Order.objects.get(id=self.order.id)
        self.claim.save()
        self.assertEqual(Claim.objects.first(), self.claim)

    def test_can_create_marketing_in_database(self):
        MONTH_DURATION = 1
        self.marketing.customer_segment = "Nouvelle Inscription"
        self.marketing.description = "Une première campagne de marketing"
        self.marketing.start_date = datetime.now()
        self.marketing.end_date = self.marketing.start_date.replace(month=self.marketing.start_date.month + MONTH_DURATION)
        self.marketing.save()
        self.assertEqual(Marketing.objects.first(), self.marketing)

    def helper_save_order_in_database(self):
        """ Saves an order into the database """
        self.order.date = datetime.now()
        self.order.customer = Customer.objects.get(id=self.customer.id)
        self.order.product = Product.objects.get(id=self.customer.id)
        self.order.save()

    def helper_create_customer(self):
        """ Creates a sample customer object """
        new_customer = Customer()
        new_customer.name = "Yan Solo"
        new_customer.customer_type="Particulier"
        new_customer.dob = "1977-07-01"
        new_customer.gender = "Masculin"
        new_customer.email = "yansolo@gmail.com"
        new_customer.phone = "0678295432"
        new_customer.address = "12 avenue Henri-Martin"
        new_customer.town = "Paris"
        new_customer.region = "IDF"
        new_customer.date_created = datetime.now()

        return new_customer

    def helper_create_product(self):
        """ Creates a sample product object """
        new_product = Product()
        new_product.name = "PC Dell 1"
        new_product.description = "Un premier PC Dell"
        new_product.category = "Informatique"
        new_product.n_lot = "123456"
        new_product.price_pdt_HT = 1299.99
        new_product.commercial_margin = 200.0
        new_product.stock_q = 12
        new_product.stock_security = 5

        return new_product