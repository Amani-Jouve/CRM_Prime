from django.test import TestCase
from django.http import HttpRequest
from django.db import models
from django.utils import timezone
from .models import Customer, Product, Order, Claim, Marketing
from .views import create_customers, create_products, create_orders, create_claims, create_marketing
from datetime import datetime
from .helper_test_methods import helper_create_customer, helper_create_product, helper_create_order, helper_create_claim, helper_create_marketing


class FormsTest(TestCase):
    def setUp(self):
        self.customer = helper_create_customer()
        self.product = helper_create_product()

    def tearDown(self):
        pass

    def test_customer_form_can_save_POST_request(self):
        customer = self.customer

        request = HttpRequest()
        request.method = "POST"
        request.POST["name"] = customer.name
        request.POST["customer_type"] = customer.customer_type
        request.POST["dob"] = customer.dob
        request.POST["gender"] = customer.gender
        request.POST["email"] = customer.email
        request.POST["phone"] = customer.phone
        request.POST["address"] = customer.address
        request.POST["town"] = customer.town
        request.POST["region"] = customer.region
        request.POST["date_created"] = customer.date_created
        response = create_customers(request)
        self.assertEqual(Customer.objects.count(), 1)

        posted_customer = Customer.objects.first()

        self.assertEqual(customer.name, posted_customer.name)
        self.assertEqual(customer.customer_type, posted_customer.customer_type)
        self.assertEqual(customer.dob, posted_customer.dob)
        self.assertEqual(customer.gender, posted_customer.gender)
        self.assertEqual(customer.email, posted_customer.email)
        self.assertEqual(customer.phone, posted_customer.phone)
        self.assertEqual(customer.address, posted_customer.address)
        self.assertEqual(customer.town, posted_customer.town)
        self.assertEqual(customer.region, posted_customer.region)
        # TO DO: better test: approx. equal ?
        # fix me: automatically created field ?
        # self.assertTrue(customer.date_created < posted_customer.date_created)


    def test_product_form_can_save_POST_request(self):
        product = self.product
        request = HttpRequest()
        request.method = "POST"
        request.POST["name"] = product.name
        request.POST["description"] = product.description
        request.POST["category"] = product.category
        request.POST["n_lot"] = product.n_lot
        request.POST["price_pdt_HT"] = product.price_pdt_HT
        request.POST["commercial_margin"] = product.commercial_margin
        request.POST["stock_q"] = product.stock_q
        request.POST["stock_security"] = product.stock_security
        response = create_products(request)
        self.assertEqual(Product.objects.count(), 1)

        posted_product = Product.objects.first()

        self.assertEqual(product.name, posted_product.name)
        self.assertEqual(product.category, posted_product.category)
        self.assertEqual(product.n_lot, posted_product.n_lot)
        self.assertEqual(product.price_pdt_HT, posted_product.price_pdt_HT)
        self.assertEqual(product.commercial_margin, posted_product.commercial_margin)
        self.assertEqual(product.stock_q, posted_product.stock_q)
        self.assertEqual(product.stock_security, posted_product.stock_security)


    def test_order_form_can_save_POST_request(self):
        self.customer = helper_create_customer()
        self.customer.save()
        self.product = helper_create_product()
        self.product.save()

        new_order = helper_create_order(self.customer, self.product)

        date_now = self.get_timezone_aware_now()


        request = HttpRequest()
        request.method = "POST"
        request.POST["customer"] = Customer.objects.get(id=self.customer.id)
        request.POST["product"] = Product.objects.get(id=self.product.id)
        request.POST["date"] = date_now
        request.POST["quantity"] = new_order.quantity
        request.POST["discount"] = new_order.discount
        request.POST["date_created"] = new_order.date
        request.POST["status"] = new_order.status
        request.POST["Delivery_date_expected"] = new_order.Delivery_date_expected
        request.POST["satisfaction_score"] = new_order.satisfaction_score
        response = create_orders(request)
        self.assertEqual(Order.objects.count(), 1)

        posted_order = Order.objects.first()

        self.assertEquals(self.customer, posted_order.customer)
        self.assertEquals(self.product, posted_order.product)
#       TO DO: dates
        self.assertEquals(new_order.date, posted_order.date)
        self.assertEquals(new_order.quantity, posted_order.quantity)
        self.assertEquals(new_order.discount, posted_order.discount)


        # TO DO : better test
    #    print(new_order.date_created, posted_order.date_created)
    #    self.assertTrue(new_order.date_created < posted_order.date_created)

        self.assertEquals(new_order.status, posted_order.status)
#       TO DO : timezones
        self.assertEquals(new_order.Delivery_date_expected, posted_order.Delivery_date_expected)
        self.assertEquals(new_order.satisfaction_score, posted_order.satisfaction_score)

    def test_claim_form_can_save_POST_request(self):
        self.customer = helper_create_customer()
        self.customer.save()
        self.product = helper_create_product()
        self.product.save()
        self.order = helper_create_order(self.customer, self.product)
        self.order.save()

        new_claim = self.helper_create_claim(self.customer, self.product)   

        request = HttpRequest()
        request.method = "POST"
        request.POST["customer"] = Customer.objects.get(id=self.customer.id)
        request.POST["order"] = Order.objects.get(id=self.product.id)
        request.POST["date"] = new_claim.date
        request.POST["date_created"] = new_claim.date_created
        request.POST["description"] = new_claim.description
        request.POST["Operator"] = new_claim.Operator
        request.POST["Type"] = new_claim.Type
        request.POST["action"] = new_claim.action
        request.POST["status"] = new_claim.status
        request.POST["resolution_date_expected"] = new_claim.resolution_date_expected
        request.POST["last_contact_customer_date"] = self.get_timezone_aware_now()

        response = create_claims(request)
        self.assertEqual(Claim.objects.count(), 1)

        posted_claim = Claim.objects.first()

        self.assertEquals(new_claim.customer, posted_claim.customer)
        self.assertEquals(new_claim.order, posted_claim.order)
#       TO DO: timezones
        print(new_claim.date_created, posted_claim.date_created)
#        self.assertTrue(new_claim.date_created < posted_claim.date_created)
        self.assertEquals(new_claim.description, posted_claim.description)
        self.assertEquals(new_claim.Operator, posted_claim.Operator)
        self.assertEquals(new_claim.Type, posted_claim.Type)
        self.assertEquals(new_claim.action, posted_claim.action)
        self.assertEquals(new_claim.status, posted_claim.status)
#       TO DO: timezones
        self.assertEquals(new_claim.resolution_date_expected, posted_claim.resolution_date_expected)

        # TO DO: solve NoneType problem
#        self.assertTrue(claim.last_contact_customer_date < posted_claim.last_contact_customer_date)


    def test_marketing_form_can_save_POST_request(self):
        new_marketing = self.helper_create_marketing()

        request = HttpRequest()
        request.method = "POST"
        request.POST["customer_segment"] = new_marketing.customer_segment
        request.POST["description"] = new_marketing.description
        request.POST["start_date"] = new_marketing.start_date
        request.POST["end_date"] = new_marketing.end_date

        response = create_marketing(request)
        self.assertEqual(Marketing.objects.count(), 1)

        posted_marketing = Marketing.objects.first()

        self.assertEquals(new_marketing.customer_segment, posted_marketing.customer_segment)
        self.assertEquals(new_marketing.description, posted_marketing.description)

        self.assertEquals(new_marketing.start_date, posted_marketing.start_date)
        self.assertEquals(new_marketing.end_date, posted_marketing.end_date)


    def helper_create_claim(self, customer, product):
        """ Creates a sample claim object """
        RES_DELAY = 3
        date_now = self.get_timezone_aware_now()
        res_date_expected = date_now.replace(day=date_now.day + RES_DELAY)

        new_claim = Claim()
        new_claim.customer = Customer.objects.get(id=customer.id)
        new_claim.order = Order.objects.get(id=product.id)
        new_claim.date = date_now
        new_claim.date_created = date_now
        new_claim.description = "Une première réclamation"
        new_claim.Operator = "Amani"
        new_claim.Type = "article erronné"
        new_claim.action = "Changer l'article"
        new_claim.status = "ouverte"
        new_claim.resolution_date_expected = res_date_expected

        return new_claim

    def helper_create_marketing(self):
        """ Creates a sample marketing object """
        CAMPAIGN_DURATION=1
        date_now = self.get_timezone_aware_now()
        end_date = date_now.replace(month=date_now.month + CAMPAIGN_DURATION)

        new_marketing = Marketing()
        new_marketing.customer_segment = "Potentiel moyen"
        new_marketing.description = "Une nouvelle campagne de marketing"
        new_marketing.start_date = date_now
        new_marketing.end_date = end_date

        return new_marketing

    def get_timezone_aware_now(self):
        return timezone.make_aware(datetime.now())
        
