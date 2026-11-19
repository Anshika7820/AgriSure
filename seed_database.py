"""
AgriSure Master Database Seeder
===============================
Seeds all data required for demonstration, presentations, and automated tests:
1. Users & Profiles (admin, farmer1, farmer2, buyer1, buyer2)
2. Categories & Verified Farms
3. 10 High-Quality Crop Listings with 100% matched local photos
4. Negotiations & Forward Contracts
5. Deliveries & Milestone Payments
6. Admin Arbitration (Disputes, Pending Document Verifications, Audit Logs)
7. Ready-to-Test Action Fixtures (Pending Contract for Signing, Pending Payment for Razorpay Checkout)
"""

import os
import django
from decimal import Decimal
from datetime import date, timedelta
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
    print("=" * 60)
    print("AgriSure Master Database Seeding Starting...")
    print("=" * 60)

    # -------------------------------------------------------------
    # 1. Superuser / Admin
    # -------------------------------------------------------------
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
        print("[+] Created Superuser: admin / admin@123")
    else:
        admin_user = User.objects.get(username="admin")

    # -------------------------------------------------------------
    # 2. Farmers
    # -------------------------------------------------------------
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
            total_land_acres=Decimal("25.50"),
            primary_crops="Wheat, Basmati Rice, Mustard",
            experience_years=18,
            upi_id="gurpreet.singh@okaxis",
            bank_account_number="987654321001",
            ifsc_code="PUNB0123400"
        )
        print("[+] Created Farmer: farmer1 (Gurpreet Singh)")
    else:
        farmer1 = User.objects.get(username="farmer1")

    if not User.objects.filter(username="farmer2").exists():
        farmer2 = User.objects.create_user(
            username="farmer2",
            email="ramesh@agrisure.in",
            password="farmer@123",
            role=User.Role.FARMER,
            first_name="Ramesh Patel",
            phone="+91 98765 43211",
            is_verified=True
        )
        FarmerProfile.objects.create(
            user=farmer2,
            farm_name="Patel Organic Farms",
            village="Sanand",
            district="Ahmedabad",
            state="Gujarat",
            total_land_acres=Decimal("40.00"),
            primary_crops="Cotton, Turmeric, Cumin",
            experience_years=12,
            upi_id="ramesh.patel@okhdfcbank",
            bank_account_number="987654321002",
            ifsc_code="HDFC0001234"
        )
        print("[+] Created Farmer: farmer2 (Ramesh Patel)")
    else:
        farmer2 = User.objects.get(username="farmer2")

    # -------------------------------------------------------------
    # 3. Buyers
    # -------------------------------------------------------------
    if not User.objects.filter(username="buyer1").exists():
        buyer1 = User.objects.create_user(
            username="buyer1",
            email="procurement@annapurnafoods.in",
            password="buyer@123",
            role=User.Role.BUYER,
            first_name="Annapurna Agro Industries Pvt Ltd",
            phone="+91 91234 56780",
            is_verified=True
        )
        BuyerProfile.objects.create(
            user=buyer1,
            company_name="Annapurna Agro Industries Pvt Ltd",
            business_type=BuyerProfile.BusinessType.PROCESSOR,
            gstin="07AAAAA1234A1Z5",
            pan_number="AAAAA1234A",
            registered_address="Plot 44, Food Processing Park, Rai Industrial Area",
            city="Sonipat",
            state="Haryana",
            pincode="131029",
            contact_person_name="Vikram Mehta",
            contact_person_phone="+91 91234 56780"
        )
        print("[+] Created Buyer: buyer1 (Annapurna Agro Industries)")
    else:
        buyer1 = User.objects.get(username="buyer1")

    if not User.objects.filter(username="buyer2").exists():
        buyer2 = User.objects.create_user(
            username="buyer2",
            email="trade@nationalexports.com",
            password="buyer@123",
            role=User.Role.BUYER,
            first_name="National Grain & Spice Exports",
            phone="+91 91234 56781",
            is_verified=True
        )
        BuyerProfile.objects.create(
            user=buyer2,
            company_name="National Grain & Spice Exports",
            business_type=BuyerProfile.BusinessType.EXPORTER,
            gstin="27BBBBB5678B1Z2",
            pan_number="BBBBB5678B",
            registered_address="Export Bhavan, Sector 18, Vashi",
            city="Navi Mumbai",
            state="Maharashtra",
            pincode="400703",
            contact_person_name="Pooja Sharma",
            contact_person_phone="+91 91234 56781"
        )
        print("[+] Created Buyer: buyer2 (National Grain & Spice Exports)")
    else:
        buyer2 = User.objects.get(username="buyer2")

    # -------------------------------------------------------------
    # 4. Farms
    # -------------------------------------------------------------
    farm1, _ = Farm.objects.get_or_create(
        farmer=farmer1,
        farm_name="Khanna North Estate",
        defaults={
            "survey_number": "KHN-45/1",
            "village": "Khanna Kalan",
            "district": "Ludhiana",
            "state": "Punjab",
            "area_acres": Decimal("15.00"),
            "soil_type": "Alluvial Loam",
            "irrigation_source": "Tube Well & Canal Network"
        }
    )

    farm2, _ = Farm.objects.get_or_create(
        farmer=farmer2,
        farm_name="Sanand Agro Farm",
        defaults={
            "survey_number": "SND-102/3",
            "village": "Sanand",
            "district": "Ahmedabad",
            "state": "Gujarat",
            "area_acres": Decimal("22.50"),
            "soil_type": "Black Cotton Soil",
            "irrigation_source": "Drip Irrigation & Narmada Canal"
        }
    )

    farm_south, _ = Farm.objects.get_or_create(
        farmer=farmer2,
        farm_name="Malabar & Konkan Plantation Estate",
        defaults={
            "survey_number": "PLOT-77/A",
            "village": "Wayanad Hills",
            "district": "Wayanad",
            "state": "Kerala",
            "area_acres": Decimal("25.0"),
            "soil_type": "Rich Red Laterite & Forest Loam",
            "irrigation_source": "Drip Micro-Sprinkler & Mountain Spring",
        }
    )

    # -------------------------------------------------------------
    # 5. Crop Categories
    # -------------------------------------------------------------
    cereals, _ = CropCategory.objects.get_or_create(
        name="Cereals & Grains",
        defaults={"description": "Staple food grains including Wheat, Rice, Maize, Barley, and Millets.", "icon": "bi-flower1"}
    )
    pulses, _ = CropCategory.objects.get_or_create(
        name="Pulses & Legumes",
        defaults={"description": "High-protein legumes: Chickpeas, Lentils, Pigeon Peas, Black Gram.", "icon": "bi-circle-square"}
    )
    oilseeds, _ = CropCategory.objects.get_or_create(
        name="Oilseeds",
        defaults={"description": "Commercial oil crops: Mustard, Soybean, Groundnut, Sunflower, Sesame.", "icon": "bi-droplet"}
    )
    commercial, _ = CropCategory.objects.get_or_create(
        name="Commercial & Fiber",
        defaults={"description": "Industrial cash crops: Cotton, Sugarcane, Jute, Tobacco.", "icon": "bi-cash-coin"}
    )
    spices, _ = CropCategory.objects.get_or_create(
        name="Vegetables & Spices",
        defaults={"description": "Spices and high-value perishables: Turmeric, Chilli, Cumin, Coriander.", "icon": "bi-fire"}
    )
    horticulture, _ = CropCategory.objects.get_or_create(
        name="Horticulture & Fruits",
        defaults={"description": "High value fresh orchard produce, GI-tagged fruits, and plantation crops.", "icon": "bi-apple"}
    )

    # -------------------------------------------------------------
    # 6. Complete Crop Listings (10 Presentation Crops with Photos)
    # -------------------------------------------------------------
    today = date.today()

    crops_catalog = [
        {
            "crop_name": "Sharbati Premium Wheat",
            "farmer": farmer1,
            "farm": farm1,
            "category": cereals,
            "variety": "MP Sharbati Gold (C-306)",
            "total_quantity_kg": Decimal("10000.00"),
            "expected_price_per_kg": Decimal("32.50"),
            "quality_grade": "Grade A+ (Premium Golden Grain)",
            "harvest_days": 45,
            "description": "Rainfed Sharbati wheat grown under organic bio-fertilizer protocol. Heavy golden grain with protein content exceeding 13.5%.",
            "crop_image": "crops/sharbati_premium_wheat.jpg"
        },
        {
            "crop_name": "Traditional Basmati Rice 1121",
            "farmer": farmer1,
            "farm": farm1,
            "category": cereals,
            "variety": "Pusa Basmati 1121 (Aged 1 Year)",
            "total_quantity_kg": Decimal("8000.00"),
            "expected_price_per_kg": Decimal("65.00"),
            "quality_grade": "Export Grade (Avg Grain Length 8.35mm)",
            "harvest_days": 60,
            "description": "Authentic Punjab export-quality 1121 long-grain Basmati. Naturally aged, minimal broken grain percentage (< 2%), high elongation ratio.",
            "crop_image": "crops/traditional_basmati_rice_1121.jpg"
        },
        {
            "crop_name": "Organic Bt Cotton (Long Staple)",
            "farmer": farmer2,
            "farm": farm2,
            "category": commercial,
            "variety": "Shankar-6 (Staple Length 30mm+)",
            "total_quantity_kg": Decimal("6000.00"),
            "expected_price_per_kg": Decimal("78.00"),
            "quality_grade": "Grade A (Micronaire 3.8-4.2)",
            "harvest_days": 30,
            "description": "Clean, hand-picked long staple Gujarat Shankar-6 cotton with low trash content (< 2.5%). Ideal for spinning mills.",
            "crop_image": "crops/organic_bt_cotton_(long_staple).jpg"
        },
        {
            "crop_name": "Yellow Mustard (Pusa Bold)",
            "farmer": farmer1,
            "farm": farm1,
            "category": oilseeds,
            "variety": "Pusa Bold (High Oil Content)",
            "total_quantity_kg": Decimal("5000.00"),
            "expected_price_per_kg": Decimal("54.00"),
            "quality_grade": "Oil Grade 1 (42% Lab-Tested Oil Yield)",
            "harvest_days": 20,
            "description": "High pungency mustard seeds with 42%+ certified oil yield. Zero chemical residue, dried to < 8% moisture.",
            "crop_image": "crops/yellow_mustard_(pusa_bold).jpg"
        },
        {
            "crop_name": "Salem Turmeric Fingers",
            "farmer": farmer2,
            "farm": farm2,
            "category": spices,
            "variety": "Salem High-Curcumin Bold",
            "total_quantity_kg": Decimal("3000.00"),
            "expected_price_per_kg": Decimal("135.00"),
            "quality_grade": "Export Grade (Curcumin 4.8%+)",
            "harvest_days": 90,
            "description": "Sun-dried Salem finger turmeric. Vibrant yellow color, polished, double-cleaned with guaranteed 4.8% curcumin content.",
            "crop_image": "crops/salem_turmeric_fingers.jpg"
        },
        {
            "crop_name": "Guntur Teja Red Chilli",
            "farmer": farmer2,
            "farm": farm_south,
            "category": spices,
            "variety": "S-17 Teja Export Grade",
            "total_quantity_kg": Decimal("4000.00"),
            "expected_price_per_kg": Decimal("210.00"),
            "quality_grade": "Export Grade (Max 10% Moisture, High Heat)",
            "harvest_days": 15,
            "description": "High capsaicin content (0.5%+) vibrant crimson red chillies sun-dried on clean tarpaulins. Rigorously tested for zero aflatoxin residue.",
            "crop_image": "crops/guntur_teja_red_chilli.jpg"
        },
        {
            "crop_name": "Ratnagiri Alphonso Mangoes",
            "farmer": farmer2,
            "farm": farm_south,
            "category": horticulture,
            "variety": "GI Tag Certified Hapus",
            "total_quantity_kg": Decimal("3500.00"),
            "expected_price_per_kg": Decimal("140.00"),
            "quality_grade": "Grade A+ (Export Quality 250g+)",
            "harvest_days": 25,
            "description": "Authentic GI-registered Devgad/Ratnagiri Hapus mangoes naturally tree-ripened without chemical calcium carbide. Rich saffron aroma and fiberless pulp.",
            "crop_image": "crops/ratnagiri_alphonso_mangoes.jpg"
        },
        {
            "crop_name": "Organic Desi Chickpeas (Chana)",
            "farmer": farmer1,
            "farm": farm1,
            "category": pulses,
            "variety": "JG-11 Bold Gold Grain",
            "total_quantity_kg": Decimal("8000.00"),
            "expected_price_per_kg": Decimal("68.00"),
            "quality_grade": "Machine Cleaned 99.5% Purity",
            "harvest_days": 30,
            "description": "Non-GMO organic brown desi chickpeas grown in deep black cotton soils under integrated pest management. High protein 22%+, ideal for besan milling and packaging.",
            "crop_image": "crops/organic_desi_chickpeas.jpg"
        },
        {
            "crop_name": "Malabar Tellicherry Black Pepper",
            "farmer": farmer2,
            "farm": farm_south,
            "category": spices,
            "variety": "TGSEB Extra Bold (4.75mm+)",
            "total_quantity_kg": Decimal("1200.00"),
            "expected_price_per_kg": Decimal("620.00"),
            "quality_grade": "Export Garbled Extra Bold",
            "harvest_days": 40,
            "description": "World-famous Malabar black pepper hand-harvested from shaded hill slopes of Wayanad. High piperine, intense pungency, and natural sun-dried aroma.",
            "crop_image": "crops/malabar_black_pepper.jpg"
        },
        {
            "crop_name": "Shimla Royal Delicious Apples",
            "farmer": farmer1,
            "farm": farm1,
            "category": horticulture,
            "variety": "Grade A Royal Delicious",
            "total_quantity_kg": Decimal("5000.00"),
            "expected_price_per_kg": Decimal("115.00"),
            "quality_grade": "Export Grade (75-85mm Caliber)",
            "harvest_days": 18,
            "description": "Crisp, juicy mountain apples cultivated at 7,000 ft altitude in Shimla valley. Plucked at peak brix sugar level, sorted into standard corrugated trays.",
            "crop_image": "crops/shimla_royal_delicious_apples.jpg"
        }
    ]

    for item in crops_catalog:
        crop, created = CropListing.objects.update_or_create(
            crop_name=item["crop_name"],
            defaults={
                "farmer": item["farmer"],
                "farm": item["farm"],
                "category": item["category"],
                "variety": item["variety"],
                "total_quantity_kg": item["total_quantity_kg"],
                "available_quantity_kg": item["total_quantity_kg"],
                "expected_price_per_kg": item["expected_price_per_kg"],
                "quality_grade": item["quality_grade"],
                "expected_harvest_date": today + timedelta(days=item["harvest_days"]),
                "available_from": today + timedelta(days=item["harvest_days"] + 5),
                "description": item["description"],
                "crop_image": item["crop_image"],
                "status": CropListing.Status.ACTIVE
            }
        )
        tag = "[+] Added" if created else "[~] Updated"
        print(f"{tag} Crop: {crop.crop_name} (Image: {crop.crop_image})")

    # -------------------------------------------------------------
    # 7. Offers & Active Forward Contract
    # -------------------------------------------------------------
    crop_wheat = CropListing.objects.filter(crop_name__icontains="Wheat").first()
    crop_rice = CropListing.objects.filter(crop_name__icontains="Basmati").first()

    offer1, _ = Offer.objects.get_or_create(
        crop_listing=crop_wheat,
        buyer=buyer1,
        defaults={
            "quantity_kg": Decimal("5000.00"),
            "proposed_price_per_kg": Decimal("31.50"),
            "delivery_date": today + timedelta(days=50),
            "delivery_location": "Annapurna Food Processing Unit 2, Rai Industrial Area, Sonipat",
            "quality_specifications": "Moisture <= 11.5%, Foreign matter <= 0.5%, Minimum test weight 78 kg/hL.",
            "message": "We can offer ₹31.50/kg for a guaranteed 5-ton lot delivery directly to our Sonipat plant.",
            "status": Offer.Status.ACCEPTED,
            "current_turn": Offer.Turn.NONE
        }
    )

    contract1, c_created = Contract.objects.get_or_create(
        contract_number="AGRI-2026-WHT-001",
        defaults={
            "offer": offer1,
            "farmer": farmer1,
            "buyer": buyer1,
            "crop_name": crop_wheat.crop_name,
            "variety": crop_wheat.variety,
            "quantity_kg": Decimal("5000.00"),
            "agreed_price_per_kg": Decimal("31.50"),
            "total_value": Decimal("157500.00"),
            "advance_amount": Decimal("15750.00"),
            "delivery_schedule": f"Single bulk delivery by {(today + timedelta(days=50)).strftime('%d-%b-%Y')}.",
            "delivery_location": "Annapurna Processing Unit 2, Rai Industrial Area, Sonipat, Haryana",
            "quality_specifications": "Moisture <= 11.5%, Foreign matter <= 0.5%, Minimum test weight 78 kg/hL.",
            "status": Contract.Status.ACTIVE,
            "farmer_accepted": True,
            "buyer_accepted": True,
            "farmer_accepted_at": timezone.now() - timedelta(days=5),
            "buyer_accepted_at": timezone.now() - timedelta(days=5)
        }
    )
    print(f"[+] Contract Active: {contract1.contract_number}")

    # Deliveries
    Delivery.objects.get_or_create(
        contract=contract1,
        delivery_number="DEL-AGRI-WHT-01",
        defaults={
            "scheduled_date": today + timedelta(days=15),
            "quantity_scheduled_kg": Decimal("2500.00"),
            "status": Delivery.Status.SCHEDULED,
            "delivery_notes": "Advance transit preparation. Consignment assigned to Central Trans Logistics."
        }
    )

    # Payments for Contract 1
    Payment.objects.get_or_create(
        contract=contract1,
        payment_type=Payment.PaymentType.ADVANCE,
        defaults={
            "payer": buyer1,
            "recipient": farmer1,
            "amount": Decimal("15750.00"),
            "status": Payment.Status.SUCCESS,
            "gateway_order_id": "order_MOCK_AGRI_ADV_001",
            "gateway_payment_id": "pay_MOCK_ADVANCE_CONFIRMED",
            "paid_at": timezone.now() - timedelta(days=4),
            "notes": "10% Advance Security Escrow deposited successfully."
        }
    )

    # -------------------------------------------------------------
    # 8. Pending Action Fixtures (For Live Demo & Razorpay Test)
    # -------------------------------------------------------------
    offer_rice, _ = Offer.objects.get_or_create(
        crop_listing=crop_rice,
        buyer=buyer1,
        defaults={
            "proposed_price_per_kg": Decimal("64.00"),
            "quantity_kg": Decimal("2500"),
            "delivery_date": today + timedelta(days=20),
            "delivery_location": "Sonepat Modern Rice Milling & Storage Terminal, Haryana",
            "quality_specifications": "Extra Long Grain Basmati 1121, Max 11.5% moisture, 100% sortex clean.",
            "status": Offer.Status.ACCEPTED,
            "current_turn": Offer.Turn.NONE
        }
    )

    contract_pending, _ = Contract.objects.get_or_create(
        contract_number="AGRI-2026-RICE-002",
        defaults={
            "offer": offer_rice,
            "farmer": farmer1,
            "buyer": buyer1,
            "crop_name": crop_rice.crop_name,
            "variety": crop_rice.variety,
            "quantity_kg": Decimal("2500"),
            "agreed_price_per_kg": Decimal("64.00"),
            "total_value": Decimal("160000.00"),
            "advance_amount": Decimal("16000.00"),
            "delivery_location": offer_rice.delivery_location,
            "delivery_schedule": f"Fulfillment scheduled on or before {(today + timedelta(days=20)).strftime('%d-%b-%Y')}.",
            "quality_specifications": offer_rice.quality_specifications,
            "status": Contract.Status.PROPOSED,
            "farmer_accepted": False,
            "buyer_accepted": False
        }
    )
    # Reset to proposed to allow demonstration of signing
    contract_pending.status = Contract.Status.PROPOSED
    contract_pending.farmer_accepted = False
    contract_pending.buyer_accepted = False
    contract_pending.farmer_accepted_at = None
    contract_pending.buyer_accepted_at = None
    contract_pending.save()
    print(f"[+] Pending Contract for Signing: {contract_pending.contract_number} (ID: {contract_pending.id})")

    # Pending payment for Razorpay checkout demo
    p_pending = Payment.objects.filter(contract=contract1, status=Payment.Status.PENDING).first()
    if not p_pending:
        p_pending = Payment.objects.create(
            contract=contract1,
            payer=buyer1,
            recipient=farmer1,
            amount=Decimal("45000.00"),
            payment_type=Payment.PaymentType.FINAL,
            status=Payment.Status.PENDING,
            notes="Milestone final settlement tranche for Contract #AGRI-2026-WHT-001"
        )
        print(f"[+] Pending Payment #{p_pending.id} ready for Razorpay checkout testing.")

    # -------------------------------------------------------------
    # 9. Admin Arbitration Fixtures (Disputes & Verifications)
    # -------------------------------------------------------------
    if not VerificationDocument.objects.filter(user=farmer2).exists():
        VerificationDocument.objects.create(
            user=farmer2,
            document_type="Revenue Land Record (Khasra-Khatauni / 7-12 Extract)",
            status=VerificationDocument.Status.PENDING,
            admin_notes=""
        )
        farmer2.is_verified = False
        farmer2.save(update_fields=["is_verified"])
        print("[+] Created Pending Verification Document for farmer2")

    if not VerificationDocument.objects.filter(user=buyer2).exists():
        VerificationDocument.objects.create(
            user=buyer2,
            document_type="FSSAI Wholesale Manufacturing & Export License",
            status=VerificationDocument.Status.PENDING,
            admin_notes=""
        )
        buyer2.is_verified = False
        buyer2.save(update_fields=["is_verified"])
        print("[+] Created Pending Verification Document for buyer2")

    # Approved documents for farmer1 & buyer1
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

    # Dispute for admin arbitration
    if not Dispute.objects.filter(contract=contract1).exists():
        dispute = Dispute.objects.create(
            contract=contract1,
            raised_by=buyer1,
            reason=Dispute.ReasonCategory.QUALITY,
            description="Batch moisture reading during pre-shipment quality inspection recorded 12.8%, which is slightly above the contractually stipulated 11.5% maximum threshold. Requesting joint sampling or platform quality re-testing.",
            status=Dispute.Status.OPEN
        )
        AuditLog.log("DISPUTE_RAISED", "Dispute", dispute.id, f"Buyer {buyer1.username} raised Quality dispute #{dispute.id} on Contract {contract1.contract_number}", user=buyer1)
        print(f"[+] Created sample Dispute #{dispute.id} on {contract1.contract_number}")

    # Reviews
    Review.objects.get_or_create(
        contract=contract1,
        reviewer=buyer1,
        defaults={
            "reviewed_party": farmer1,
            "rating": 5,
            "comment": "Exceptional grain quality! Gurpreet Singh provided regular crop progress updates and transparent moisture lab certificates."
        }
    )

    # Notifications
    Notification.objects.get_or_create(
        recipient=farmer1,
        title="Active Contract Enforced: AGRI-2026-WHT-001",
        defaults={
            "message": "Both parties signed Contract #AGRI-2026-WHT-001. Advance payment is secured.",
            "notification_type": "CONTRACT",
            "link_url": f"/contracts/{contract1.id}/",
            "is_read": False
        }
    )

    AuditLog.log("SYSTEM_SEEDED", "Platform", 0, "Master database seed executed successfully.")

    print("=" * 60)
    print("[SUCCESS] AgriSure Database successfully seeded!")
    print(f"Total Crops: {CropListing.objects.count()} (100% with photos)")
    print(f"Total Contracts: {Contract.objects.count()}")
    print("--------------------------------------------------")
    print("DEMO CREDENTIALS:")
    print("  Administrator : admin    / admin@123")
    print("  Farmer        : farmer1  / farmer@123")
    print("  Buyer         : buyer1   / buyer@123")
    print("=" * 60)


if __name__ == "__main__":
    seed()
