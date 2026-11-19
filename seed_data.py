"""
AgriSure Data Seeder: Populates initial realistic crop categories, demo accounts,
farms, crop listings, forward contracts, deliveries, and notifications.
"""

import os
import django
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.models import User, FarmerProfile, BuyerProfile, VerificationDocument
from farms.models import Farm
from marketplace.models import CropCategory, CropListing
from negotiations.models import Offer, NegotiationMessage
from contracts.models import Contract
from deliveries.models import Delivery
from payments.models import Payment
from notifications.models import Notification
from disputes.models import Dispute
from reviews.models import Review
from audit.models import AuditLog

def seed():
    print("Seeding AgriSure platform database...")

    # 1. Superuser / Admin
    if not User.objects.filter(username="admin").exists():
        admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@agrisure.in",
            password="admin@123",
            role=User.Role.ADMIN,
            first_name="Platform Administrator",
            is_verified=True,
            phone="+91 98000 00000"
        )
        print("Created Superuser: admin / admin@123")
    else:
        admin_user = User.objects.get(username="admin")

    # 2. Farmer 1: Gurpreet Singh (Punjab)
    if not User.objects.filter(username="farmer1").exists():
        farmer1 = User.objects.create_user(
            username="farmer1",
            email="gurpreet@agrisure.in",
            password="farmer@123",
            role=User.Role.FARMER,
            first_name="Gurpreet Singh",
            phone="+91 98765 43210",
            is_verified=True
        )
        FarmerProfile.objects.create(
            user=farmer1,
            farm_name="Golden Fields Agri Estate",
            village="Khanna Kalan",
            district="Ludhiana",
            state="Punjab",
            postal_code="141401",
            farm_area_acres=Decimal("25.5"),
            farming_experience=14,
            primary_crops="Sharbati Wheat, Basmati Rice 1121, Mustard",
            bio="Third-generation progressive farmer practicing laser leveling, organic soil enrichment, and precision irrigation."
        )
        print("Created Farmer: farmer1 / farmer@123")
    else:
        farmer1 = User.objects.get(username="farmer1")

    # 3. Farmer 2: Ramesh Patel (Gujarat)
    if not User.objects.filter(username="farmer2").exists():
        farmer2 = User.objects.create_user(
            username="farmer2",
            email="ramesh@agrisure.in",
            password="farmer@123",
            role=User.Role.FARMER,
            first_name="Ramesh Patel",
            phone="+91 97123 45678",
            is_verified=True
        )
        FarmerProfile.objects.create(
            user=farmer2,
            farm_name="Patel Organic Agritech",
            village="Gondal",
            district="Rajkot",
            state="Gujarat",
            postal_code="360311",
            farm_area_acres=Decimal("18.0"),
            farming_experience=10,
            primary_crops="Organic Bt Cotton, Export Groundnut",
            bio="Certified organic producer equipped with drip fertigation and solar pumping systems."
        )
        print("Created Farmer: farmer2 / farmer@123")
    else:
        farmer2 = User.objects.get(username="farmer2")

    # 4. Buyer 1: Apex Agri Foods Pvt. Ltd.
    if not User.objects.filter(username="buyer1").exists():
        buyer1 = User.objects.create_user(
            username="buyer1",
            email="procurement@apexagri.com",
            password="buyer@123",
            role=User.Role.BUYER,
            first_name="Rajesh Khurana",
            phone="+91 99887 76655",
            is_verified=True
        )
        BuyerProfile.objects.create(
            user=buyer1,
            business_name="Apex Agri Foods Pvt. Ltd.",
            business_type=BuyerProfile.BusinessType.FOOD_PROCESSOR,
            contact_person="Rajesh Khurana (VP Procurement)",
            address="Plot 44-48, Sector 3, Pithampur Industrial Area",
            district="Indore",
            state="Madhya Pradesh",
            postal_code="454775",
            registration_number="23AABCA4589D1Z8"
        )
        print("Created Buyer: buyer1 / buyer@123")
    else:
        buyer1 = User.objects.get(username="buyer1")

    # 5. Buyer 2: National Grain Exports Ltd.
    if not User.objects.filter(username="buyer2").exists():
        buyer2 = User.objects.create_user(
            username="buyer2",
            email="supply@nationalexports.in",
            password="buyer@123",
            role=User.Role.BUYER,
            first_name="Ananya Sen",
            phone="+91 98111 22334",
            is_verified=True
        )
        BuyerProfile.objects.create(
            user=buyer2,
            business_name="National Grain & Spice Exports Ltd.",
            business_type=BuyerProfile.BusinessType.EXPORTER,
            contact_person="Ananya Sen (Head of Sourcing)",
            address="World Trade Tower, Barakhamba Road",
            district="New Delhi",
            state="Delhi",
            postal_code="110001",
            registration_number="07AAACN1245P1Z3"
        )
        print("Created Buyer: buyer2 / buyer@123")
    else:
        buyer2 = User.objects.get(username="buyer2")

    # 6. Farms
    farm1, _ = Farm.objects.get_or_create(
        farmer=farmer1,
        farm_name="Ludhiana Canal North Plot",
        defaults={
            "village": "Khanna",
            "district": "Ludhiana",
            "state": "Punjab",
            "postal_code": "141401",
            "area_acres": Decimal("15.5"),
            "soil_type": "Rich Alluvial Loam",
            "irrigation_source": "Sirhind Canal Branch & Solar Tubewell",
            "survey_number": "KHASRA-88/12/A"
        }
    )
    farm2, _ = Farm.objects.get_or_create(
        farmer=farmer1,
        farm_name="Ludhiana South Agro Meadow",
        defaults={
            "village": "Samrala",
            "district": "Ludhiana",
            "state": "Punjab",
            "postal_code": "141114",
            "area_acres": Decimal("10.0"),
            "soil_type": "Clayey Loam",
            "irrigation_source": "Deep Bore Tubewell",
            "survey_number": "KHASRA-104/5"
        }
    )
    farm3, _ = Farm.objects.get_or_create(
        farmer=farmer2,
        farm_name="Saurashtra Organic Cotton Tract",
        defaults={
            "village": "Gondal",
            "district": "Rajkot",
            "state": "Gujarat",
            "postal_code": "360311",
            "area_acres": Decimal("18.0"),
            "soil_type": "Medium Black Soil",
            "irrigation_source": "Drip Irrigation & Check Dam",
            "survey_number": "SURVEY-412/B"
        }
    )

    # 7. Categories
    cat_cereals, _ = CropCategory.objects.get_or_create(name="Cereals & Grains", defaults={"icon": "bi-flower1", "description": "Wheat, Rice, Maize, Millets, Barley"})
    cat_pulses, _ = CropCategory.objects.get_or_create(name="Pulses & Legumes", defaults={"icon": "bi-circle", "description": "Chickpea, Lentil, Pigeon Pea, Black Gram"})
    cat_oilseeds, _ = CropCategory.objects.get_or_create(name="Oilseeds", defaults={"icon": "bi-droplet-fill", "description": "Mustard, Soybean, Groundnut, Sunflower"})
    cat_cash, _ = CropCategory.objects.get_or_create(name="Cash Crops & Fibers", defaults={"icon": "bi-tag-fill", "description": "Cotton, Sugarcane, Jute"})
    cat_veg, _ = CropCategory.objects.get_or_create(name="Vegetables & Spices", defaults={"icon": "bi-flower2", "description": "Onion, Potato, Turmeric, Chili"})

    # 8. Crop Listings
    today = timezone.now().date()
    crop1, _ = CropListing.objects.get_or_create(
        farmer=farmer1,
        farm=farm1,
        crop_name="Sharbati Premium Wheat",
        defaults={
            "category": cat_cereals,
            "variety": "PBW-343 Certified Seed",
            "total_quantity_kg": Decimal("5000.00"),
            "available_quantity_kg": Decimal("2500.00"), # 2500 under contract!
            "expected_price_per_kg": Decimal("28.50"),
            "quality_grade": "AGMARK Grade A (Standard)",
            "expected_harvest_date": today + timedelta(days=25),
            "available_from": today + timedelta(days=30),
            "description": "High gluten (32%), golden luster, moisture strictly controlled below 11.5%. Ideal for premium branded stone-ground whole wheat atta.",
            "status": CropListing.Status.ACTIVE
        }
    )

    crop2, _ = CropListing.objects.get_or_create(
        farmer=farmer1,
        farm=farm2,
        crop_name="Traditional Basmati Rice 1121",
        defaults={
            "category": cat_cereals,
            "variety": "Pusa Basmati 1121",
            "total_quantity_kg": Decimal("8000.00"),
            "available_quantity_kg": Decimal("8000.00"),
            "expected_price_per_kg": Decimal("65.00"),
            "quality_grade": "Export Grade (Extra Long Grain)",
            "expected_harvest_date": today + timedelta(days=45),
            "available_from": today + timedelta(days=50),
            "description": "Average uncooked grain length 8.4mm with authentic aroma. Minimal broken grains (under 1%). Pesticide residue monitored per EU/US export norms.",
            "status": CropListing.Status.ACTIVE
        }
    )

    crop3, _ = CropListing.objects.get_or_create(
        farmer=farmer2,
        farm=farm3,
        crop_name="Organic Bt Cotton (Long Staple)",
        defaults={
            "category": cat_cash,
            "variety": "Bollgard II Hybrid",
            "total_quantity_kg": Decimal("4000.00"),
            "available_quantity_kg": Decimal("4000.00"),
            "expected_price_per_kg": Decimal("82.00"),
            "quality_grade": "Export Quality (29mm Staple Length)",
            "expected_harvest_date": today + timedelta(days=35),
            "available_from": today + timedelta(days=40),
            "description": "Micronaire 3.8-4.2, strength 29.5 g/tex. Trash content under 2.5%. Hand-picked to avoid contamination, zero polypropylene contamination.",
            "status": CropListing.Status.ACTIVE
        }
    )

    crop4, _ = CropListing.objects.get_or_create(
        farmer=farmer1,
        farm=farm1,
        crop_name="Yellow Mustard (Pusa Bold)",
        defaults={
            "category": cat_oilseeds,
            "variety": "Pusa Bold 42% Oil",
            "total_quantity_kg": Decimal("3500.00"),
            "available_quantity_kg": Decimal("3500.00"),
            "expected_price_per_kg": Decimal("54.00"),
            "quality_grade": "High Oil Content (41.5%+)",
            "expected_harvest_date": today + timedelta(days=20),
            "available_from": today + timedelta(days=24),
            "description": "High pungent oilseeds suitable for cold-press mustard oil extraction. Zero argemone contamination, admixture under 1.5%.",
            "status": CropListing.Status.ACTIVE
        }
    )

    crop5, _ = CropListing.objects.get_or_create(
        farmer=farmer2,
        farm=farm3,
        crop_name="Salem Turmeric Fingers",
        defaults={
            "category": cat_veg,
            "variety": "Salem High Curcumin",
            "total_quantity_kg": Decimal("2000.00"),
            "available_quantity_kg": Decimal("2000.00"),
            "expected_price_per_kg": Decimal("115.00"),
            "quality_grade": "Pharma / Spice Grade (4.8% Curcumin)",
            "expected_harvest_date": today + timedelta(days=60),
            "available_from": today + timedelta(days=70),
            "description": "Sun-dried natural yellow fingers with laboratory tested curcumin index of 4.8%. Perfect for spice processing and nutraceutical extraction.",
            "status": CropListing.Status.ACTIVE
        }
    )

    # 9. Offer 1: Accepted Offer resulting in Active Contract
    offer1, created1 = Offer.objects.get_or_create(
        crop_listing=crop1,
        buyer=buyer1,
        defaults={
            "quantity_kg": Decimal("2500.00"),
            "proposed_price_per_kg": Decimal("28.00"),
            "delivery_date": today + timedelta(days=30),
            "delivery_location": "Apex Central Food Park, Pithampur Industrial Area, Indore",
            "quality_specifications": "AGMARK Grade A, maximum moisture 11%, packed in 50kg standard polypropylene bags.",
            "message": "We propose procurement of 2,500 kg for our premium stone-ground flour processing facility.",
            "status": Offer.Status.ACCEPTED,
            "current_turn": Offer.Turn.NONE
        }
    )

    if created1:
        NegotiationMessage.objects.create(
            offer=offer1,
            sender=buyer1,
            recipient=farmer1,
            message="We propose purchase of 2,500 kg at ₹27.50/kg for prompt delivery.",
            counter_price_per_kg=Decimal("27.50"),
            counter_quantity_kg=Decimal("2500.00")
        )
        NegotiationMessage.objects.create(
            offer=offer1,
            sender=farmer1,
            recipient=buyer1,
            message="Counter: We can commit 2,500 kg at ₹28.00/kg considering quality purity certification.",
            counter_price_per_kg=Decimal("28.00"),
            counter_quantity_kg=Decimal("2500.00")
        )
        NegotiationMessage.objects.create(
            offer=offer1,
            sender=buyer1,
            recipient=farmer1,
            message="Agreed at ₹28.00/kg. Let us formulate the digital contract.",
            counter_price_per_kg=Decimal("28.00"),
            counter_quantity_kg=Decimal("2500.00")
        )

    # 10. Contract 1: Active Executed Contract
    if not Contract.objects.filter(offer=offer1).exists():
        contract1 = Contract.objects.create(
            contract_number="AGRI-2026-WHT-001",
            offer=offer1,
            farmer=farmer1,
            buyer=buyer1,
            crop_name="Sharbati Premium Wheat",
            variety="PBW-343 Certified Seed",
            quantity_kg=Decimal("2500.00"),
            agreed_price_per_kg=Decimal("28.00"),
            total_value=Decimal("70000.00"),
            delivery_location="Apex Central Food Park, Pithampur Industrial Area, Indore",
            delivery_schedule="Dispatch scheduled between 25th to 30th of month with weighbridge verification.",
            quality_specifications="AGMARK Grade A. Permissible moisture under 11.5%. Admixture under 1.5%.",
            status=Contract.Status.ACTIVE,
            farmer_accepted=True,
            farmer_accepted_at=timezone.now() - timedelta(days=2),
            farmer_digital_signature=f"SIG-F-FARMER1-SHA256-VERIFIED",
            buyer_accepted=True,
            buyer_accepted_at=timezone.now() - timedelta(days=1),
            buyer_digital_signature=f"SIG-B-BUYER1-SHA256-VERIFIED"
        )

        # Delivery 1
        Delivery.objects.create(
            contract=contract1,
            delivery_number="DEL-AGRI-WHT-01",
            scheduled_date=today + timedelta(days=15),
            quantity_scheduled_kg=Decimal("2500.00"),
            status=Delivery.Status.SCHEDULED,
            delivery_notes="Advance transit preparation. Consignment assigned to Central Trans Logistics."
        )

        # Payment 1 (Advance 15% - Settled)
        Payment.objects.create(
            contract=contract1,
            payer=buyer1,
            recipient=farmer1,
            amount=Decimal("10500.00"),
            payment_type=Payment.PaymentType.ADVANCE,
            status=Payment.Status.SUCCESS,
            payment_method="UPI / Virtual VPA Escrow Clearing",
            gateway_order_id="ORD_AGRI_ADV_001",
            gateway_payment_id="PAY_ADV_SETTLED_001",
            gateway_signature="MOCK_SIG_VERIFIED_ADVANCE_001",
            paid_at=timezone.now() - timedelta(days=1),
            notes="15% advance booking deposit settled into producer escrow account."
        )

        # Payment 2 (Milestone 85% - Pending upon delivery)
        Payment.objects.create(
            contract=contract1,
            payer=buyer1,
            recipient=farmer1,
            amount=Decimal("59500.00"),
            payment_type=Payment.PaymentType.MILESTONE,
            status=Payment.Status.PENDING,
            payment_method="Direct Bank Transfer / Escrow UPI",
            notes="85% final settlement payable within 48 hours of weighbridge scale confirmation."
        )
        print("Created Active Contract: AGRI-2026-WHT-001 (INR 70,000)")

    # 11. Offer 2: Pending Negotiation Offer on Basmati Rice
    offer2, created2 = Offer.objects.get_or_create(
        crop_listing=crop2,
        buyer=buyer2,
        defaults={
            "quantity_kg": Decimal("3000.00"),
            "proposed_price_per_kg": Decimal("62.50"),
            "delivery_date": today + timedelta(days=50),
            "delivery_location": "National Export Container Depot, Tughlakabad, Delhi",
            "quality_specifications": "Export certified grain purity 99%, pesticide residue within EU limits.",
            "message": "National Grain Exports would like to establish a forward agreement for 3,000 kg Basmati 1121 for our Gulf export shipment.",
            "status": Offer.Status.PENDING,
            "current_turn": Offer.Turn.FARMER
        }
    )

    # 12. Verification Documents
    VerificationDocument.objects.get_or_create(
        user=farmer1,
        document_type="Khasra Land Title Deed",
        defaults={
            "document_file": "documents/sample_deed.pdf",
            "status": VerificationDocument.Status.APPROVED,
            "admin_notes": "Revenue department land records verified for 25.5 acres in Khanna.",
            "reviewed_at": timezone.now()
        }
    )

    VerificationDocument.objects.get_or_create(
        user=buyer1,
        document_type="GSTIN & FSSAI Food Business License",
        defaults={
            "document_file": "documents/sample_gst.pdf",
            "status": VerificationDocument.Status.APPROVED,
            "admin_notes": "Corporate registration and FSSAI manufacturing license verified.",
            "reviewed_at": timezone.now()
        }
    )

    # 13. Notifications
    Notification.objects.get_or_create(
        recipient=farmer1,
        title="Active Contract Enforced: AGRI-2026-WHT-001",
        defaults={
            "message": "Both parties signed Contract #AGRI-2026-WHT-001. Advance payment of ₹10,500 is settled.",
            "notification_type": "CONTRACT",
            "link_url": f"/contracts/1/",
            "is_read": False
        }
    )

    Notification.objects.get_or_create(
        recipient=farmer1,
        title="New Purchase Offer Received",
        defaults={
            "message": "National Grain & Spice Exports proposed ₹62.50/kg for 3,000 kg Basmati Rice.",
            "notification_type": "OFFER",
            "link_url": f"/negotiations/offers/{offer2.id}/",
            "is_read": False
        }
    )

    Notification.objects.get_or_create(
        recipient=buyer1,
        title="Payment Settled Successfully",
        defaults={
            "message": "Advance deposit of ₹10,500 for Contract #AGRI-2026-WHT-001 verified and credited.",
            "notification_type": "PAYMENT",
            "link_url": f"/payments/1/",
            "is_read": True
        }
    )

    # 14. Audit Log
    AuditLog.log("SYSTEM_SEEDED", "Platform", 0, "Platform demonstration data successfully initialized.")

    print("\n[SUCCESS] AgriSure Database successfully seeded!")
    print("--------------------------------------------------")
    print("DEMO CREDENTIALS:")
    print("  Administrator : admin    / admin@123")
    print("  Farmer        : farmer1  / farmer@123")
    print("  Buyer         : buyer1   / buyer@123")
    print("--------------------------------------------------")

if __name__ == "__main__":
    seed()
