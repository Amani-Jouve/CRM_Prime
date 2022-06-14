from django.test import TestCase
from django.http import HttpRequest
from django.db import models
from .models import Customer, Product, Order, Claim, Marketing
from datetime import datetime
from .helper_test_methods import helper_create_customer, helper_create_product

class ModelsTest(TestCase):
    def setUp(self):
        self.customer = helper_create_customer()
        self.customer.save()

        self.product = helper_create_product()
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
