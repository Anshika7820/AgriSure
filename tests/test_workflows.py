from decimal import Decimal
from datetime import timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from accounts.models import User, FarmerProfile, BuyerProfile
from farms.models import Farm
from marketplace.models import CropCategory, CropListing
from negotiations.models import Offer, NegotiationMessage
from contracts.models import Contract
from deliveries.models import Delivery
from payments.models import Payment
from payments.services import verify_mock_or_razorpay_signature
from contracts.services import generate_contract_pdf
from disputes.models import Dispute

class AgriSureWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Farmer
        self.farmer = User.objects.create_user(
            username="test_farmer",
            email="farmer@test.com",
            password="password123",
            role=User.Role.FARMER,
            first_name="Harpreet Singh"
        )
        self.farmer_profile = FarmerProfile.objects.create(
            user=self.farmer,
            farm_name="Test Punjab Farm",
            village="Mandi",
            district="Patiala",
            state="Punjab",
            farm_area_acres=Decimal("20.0")
        )

        # Buyer
        self.buyer = User.objects.create_user(
            username="test_buyer",
            email="buyer@test.com",
            password="password123",
            role=User.Role.BUYER,
            first_name="Rajesh Agro"
        )
        self.buyer_profile = BuyerProfile.objects.create(
            user=self.buyer,
            business_name="Rajesh Agro Foods",
            business_type=BuyerProfile.BusinessType.WHOLESALER,
            address="Warehouse 5, APMC Market",
            district="Indore",
            state="Madhya Pradesh"
        )

        # Admin
        self.admin = User.objects.create_superuser(
            username="test_admin",
            email="admin@test.com",
            password="password123",
            role=User.Role.ADMIN
        )

        # Farm
        self.farm = Farm.objects.create(
            farmer=self.farmer,
            farm_name="North Field",
            village="Mandi",
            district="Patiala",
            state="Punjab",
            area_acres=Decimal("15.0")
        )

        # Category
        self.category = CropCategory.objects.create(name="Cereals")

        # Crop Listing
        self.today = timezone.now().date()
        self.crop = CropListing.objects.create(
            farmer=self.farmer,
            farm=self.farm,
            category=self.category,
            crop_name="Organic Wheat",
            variety="PBW-502",
            total_quantity_kg=Decimal("4000.00"),
            available_quantity_kg=Decimal("4000.00"),
            expected_price_per_kg=Decimal("25.00"),
            expected_harvest_date=self.today + timedelta(days=20),
            available_from=self.today + timedelta(days=25),
            status=CropListing.Status.ACTIVE
        )

    # 1. Authentication & Role Tests
    def test_farmer_registration(self):
        response = self.client.post(reverse("register_farmer"), {
            "first_name": "New Farmer",
            "username": "newfarmer",
            "email": "newfarmer@test.com",
            "phone": "9812345678",
            "password": "strongpassword123",
            "confirm_password": "strongpassword123",
            "village": "Rampur",
            "district": "Amritsar",
            "state": "Punjab",
            "farm_area_acres": "12.5",
            "farming_experience": "6",
            "agree_terms": True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newfarmer", role=User.Role.FARMER).exists())

    def test_role_based_access_controls(self):
        # Farmer cannot access buyer dashboard
        self.client.login(username="test_farmer", password="password123")
        response = self.client.get(reverse("buyer_dashboard"))
        self.assertEqual(response.status_code, 302)

        # Buyer cannot access farmer dashboard
        self.client.login(username="test_buyer", password="password123")
        response = self.client.get(reverse("farmer_dashboard"))
        self.assertEqual(response.status_code, 302)

        # Ordinary buyer cannot access admin dashboard
        response = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(response.status_code, 302)

    # 2. Marketplace & Search Tests
    def test_marketplace_listing_and_filter(self):
        response = self.client.get(reverse("marketplace"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Organic Wheat")

        # Search by crop name
        response = self.client.get(reverse("marketplace"), {"q": "Organic"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Organic Wheat")

    # 3. Offer & Negotiation Workflow
    def test_offer_submission_and_counter(self):
        self.client.login(username="test_buyer", password="password123")
        response = self.client.post(reverse("offer_create", kwargs={"crop_id": self.crop.id}), {
            "quantity_kg": 2000,
            "proposed_price_per_kg": 24.00,
            "delivery_date": self.today + timedelta(days=22),
            "delivery_location": "Indore Warehouse",
            "quality_specifications": "Standard Grade A",
            "message": "Looking for 2,000 kg"
        })
        self.assertEqual(response.status_code, 302)
        offer = Offer.objects.get(crop_listing=self.crop, buyer=self.buyer)
        self.assertEqual(offer.status, Offer.Status.PENDING)
        self.assertEqual(offer.proposed_price_per_kg, Decimal("24.00"))

        # Farmer counters offer
        self.client.login(username="test_farmer", password="password123")
        response = self.client.post(reverse("offer_counter", kwargs={"offer_id": offer.id}), {
            "counter_price_per_kg": 24.50,
            "counter_quantity_kg": 2000,
            "counter_delivery_date": self.today + timedelta(days=22),
            "message": "Can do ₹24.50/kg"
        })
        self.assertEqual(response.status_code, 302)
        offer.refresh_from_db()
        self.assertEqual(offer.status, Offer.Status.COUNTERED)
        self.assertEqual(offer.proposed_price_per_kg, Decimal("24.50"))

    # 4. Acceptance, Stock Reservation & Contract Creation
    def test_offer_accept_creates_contract_and_reserves_stock(self):
        offer = Offer.objects.create(
            crop_listing=self.crop,
            buyer=self.buyer,
            quantity_kg=Decimal("1500.00"),
            proposed_price_per_kg=Decimal("25.00"),
            delivery_date=self.today + timedelta(days=25),
            delivery_location="Indore",
            status=Offer.Status.PENDING
        )

        self.client.login(username="test_farmer", password="password123")
        response = self.client.post(reverse("offer_accept", kwargs={"offer_id": offer.id}))
        self.assertEqual(response.status_code, 302)

        # Stock reduced
        self.crop.refresh_from_db()
        self.assertEqual(self.crop.available_quantity_kg, Decimal("2500.00"))

        # Contract created
        self.assertTrue(Contract.objects.filter(offer=offer).exists())
        contract = Contract.objects.get(offer=offer)
        self.assertEqual(contract.status, Contract.Status.PROPOSED)
        self.assertEqual(contract.total_value, Decimal("37500.00"))

    # 5. Bilateral Signing, Activation & PDF Generation
    def test_contract_bilateral_signing_and_pdf(self):
        offer = Offer.objects.create(
            crop_listing=self.crop,
            buyer=self.buyer,
            quantity_kg=Decimal("1000.00"),
            proposed_price_per_kg=Decimal("25.00"),
            delivery_date=self.today + timedelta(days=25),
            delivery_location="Indore",
            status=Offer.Status.ACCEPTED
        )
        contract = Contract.objects.create(
            contract_number="AGRI-TEST-001",
            offer=offer,
            farmer=self.farmer,
            buyer=self.buyer,
            crop_name=self.crop.crop_name,
            quantity_kg=Decimal("1000.00"),
            agreed_price_per_kg=Decimal("25.00"),
            total_value=Decimal("25000.00"),
            delivery_location="Indore",
            status=Contract.Status.PROPOSED
        )

        # Farmer signs
        self.client.login(username="test_farmer", password="password123")
        self.client.post(reverse("contract_sign", kwargs={"contract_id": contract.id}), {"digital_consent": True})
        contract.refresh_from_db()
        self.assertTrue(contract.farmer_accepted)
        self.assertFalse(contract.buyer_accepted)
        self.assertEqual(contract.status, Contract.Status.PROPOSED)

        # Buyer signs -> Triggers activation & delivery + payment provisioning!
        self.client.login(username="test_buyer", password="password123")
        self.client.post(reverse("contract_sign", kwargs={"contract_id": contract.id}), {"digital_consent": True})
        contract.refresh_from_db()
        self.assertTrue(contract.buyer_accepted)
        self.assertEqual(contract.status, Contract.Status.ACTIVE)

        # Automatic Delivery & Advance payment provisioned
        self.assertTrue(Delivery.objects.filter(contract=contract).exists())
        self.assertTrue(Payment.objects.filter(contract=contract, payment_type=Payment.PaymentType.ADVANCE).exists())

        # PDF generation test
        pdf_buffer = generate_contract_pdf(contract)
        self.assertGreater(pdf_buffer.getbuffer().nbytes, 1000)

    # 6. Delivery Dispatch & Confirmation
    def test_delivery_fulfillment_flow(self):
        offer = Offer.objects.create(
            crop_listing=self.crop,
            buyer=self.buyer,
            quantity_kg=Decimal("1000.00"),
            proposed_price_per_kg=Decimal("25.00"),
            delivery_date=self.today + timedelta(days=25),
            delivery_location="Indore",
            status=Offer.Status.ACCEPTED
        )
        contract = Contract.objects.create(
            contract_number="AGRI-TEST-002",
            offer=offer,
            farmer=self.farmer,
            buyer=self.buyer,
            crop_name=self.crop.crop_name,
            quantity_kg=Decimal("1000.00"),
            agreed_price_per_kg=Decimal("25.00"),
            total_value=Decimal("25000.00"),
            delivery_location="Indore",
            status=Contract.Status.ACTIVE
        )
        delivery = Delivery.objects.create(
            contract=contract,
            delivery_number="DEL-TEST-01",
            scheduled_date=self.today + timedelta(days=5),
            quantity_scheduled_kg=Decimal("1000.00"),
            status=Delivery.Status.SCHEDULED
        )

        # Farmer dispatches
        self.client.login(username="test_farmer", password="password123")
        self.client.post(reverse("delivery_dispatch", kwargs={"delivery_id": delivery.id}), {
            "quantity_delivered_kg": 1000,
            "delivery_notes": "Truck PB-01-A-1234"
        })
        delivery.refresh_from_db()
        self.assertEqual(delivery.status, Delivery.Status.IN_TRANSIT)

        # Buyer confirms weighment
        self.client.login(username="test_buyer", password="password123")
        self.client.post(reverse("delivery_confirm", kwargs={"delivery_id": delivery.id}), {
            "decision": "CONFIRM",
            "quantity_received_kg": 1000,
            "rejection_reason": ""
        })
        delivery.refresh_from_db()
        self.assertEqual(delivery.status, Delivery.Status.CONFIRMED)

        # Contract completed since 1000/1000 fulfilled!
        contract.refresh_from_db()
        self.assertEqual(contract.status, Contract.Status.COMPLETED)

    # 7. Payment Verification & Checkout
    def test_payment_settlement_simulation(self):
        offer = Offer.objects.create(
            crop_listing=self.crop,
            buyer=self.buyer,
            quantity_kg=Decimal("1000.00"),
            proposed_price_per_kg=Decimal("25.00"),
            delivery_date=self.today + timedelta(days=25),
            delivery_location="Indore",
            status=Offer.Status.ACCEPTED
        )
        contract = Contract.objects.create(
            contract_number="AGRI-TEST-003",
            offer=offer,
            farmer=self.farmer,
            buyer=self.buyer,
            crop_name=self.crop.crop_name,
            quantity_kg=Decimal("1000.00"),
            agreed_price_per_kg=Decimal("25.00"),
            total_value=Decimal("25000.00"),
            delivery_location="Indore",
            status=Contract.Status.ACTIVE
        )
        payment = Payment.objects.create(
            contract=contract,
            payer=self.buyer,
            recipient=self.farmer,
            amount=Decimal("3750.00"),
            payment_type=Payment.PaymentType.ADVANCE,
            status=Payment.Status.PENDING
        )

        # Signature verification helper
        self.assertTrue(verify_mock_or_razorpay_signature("ORD_1", "PAY_1", "MOCK_SIG_TEST_ABC"))

        # Buyer checks out
        self.client.login(username="test_buyer", password="password123")
        response = self.client.post(reverse("payment_checkout", kwargs={"payment_id": payment.id}), {
            "payment_method": "UPI / Virtual VPA"
        })
        self.assertEqual(response.status_code, 302)
        payment.refresh_from_db()
        self.assertEqual(payment.status, Payment.Status.SUCCESS)

    # 8. Dispute Arbitration Flow
    def test_dispute_creation_and_resolution(self):
        offer = Offer.objects.create(
            crop_listing=self.crop,
            buyer=self.buyer,
            quantity_kg=Decimal("1000.00"),
            proposed_price_per_kg=Decimal("25.00"),
            delivery_date=self.today + timedelta(days=25),
            delivery_location="Indore",
            status=Offer.Status.ACCEPTED
        )
        contract = Contract.objects.create(
            contract_number="AGRI-TEST-004",
            offer=offer,
            farmer=self.farmer,
            buyer=self.buyer,
            crop_name=self.crop.crop_name,
            quantity_kg=Decimal("1000.00"),
            agreed_price_per_kg=Decimal("25.00"),
            total_value=Decimal("25000.00"),
            delivery_location="Indore",
            status=Contract.Status.ACTIVE
        )

        # Buyer files dispute
        self.client.login(username="test_buyer", password="password123")
        response = self.client.post(reverse("dispute_create", kwargs={"contract_id": contract.id}), {
            "reason": Dispute.ReasonCategory.QUALITY,
            "description": "Produce contained excessive moisture beyond agreed standard."
        })
        self.assertEqual(response.status_code, 302)
        dispute = Dispute.objects.get(contract=contract)
        self.assertEqual(dispute.status, Dispute.Status.OPEN)

        contract.refresh_from_db()
        self.assertEqual(contract.status, Contract.Status.DISPUTED)

        # Admin resolves dispute
        self.client.login(username="test_admin", password="password123")
        response = self.client.post(reverse("dispute_resolve", kwargs={"dispute_id": dispute.id}), {
            "status": Dispute.Status.RESOLVED,
            "resolution_notes": "Mediated agreement: 3% price deduction accepted by farmer."
        })
        self.assertEqual(response.status_code, 302)
        dispute.refresh_from_db()
        self.assertEqual(dispute.status, Dispute.Status.RESOLVED)
        contract.refresh_from_db()
        self.assertEqual(contract.status, Contract.Status.ACTIVE)
