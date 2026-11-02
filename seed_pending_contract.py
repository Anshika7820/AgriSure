import os
import django
from decimal import Decimal
from datetime import date, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.models import User
from marketplace.models import CropListing
from negotiations.models import Offer
from contracts.models import Contract
from payments.models import Payment

farmer1 = User.objects.get(username="farmer1")
buyer1 = User.objects.get(username="buyer1")
crop_rice = CropListing.objects.filter(crop_name__icontains="Basmati").first()

if crop_rice:
    # Create or update an accepted offer for basmati rice
    offer, created = Offer.objects.get_or_create(
        crop_listing=crop_rice,
        buyer=buyer1,
        defaults={
            "proposed_price_per_kg": Decimal("88.00"),
            "quantity_kg": Decimal("2500"),
            "delivery_date": date.today() + timedelta(days=20),
            "delivery_location": "Sonepat Modern Rice Milling & Storage Terminal, Haryana",
            "quality_specifications": "Extra Long Grain Basmati 1121, Max 11.5% moisture, 100% sortex clean.",
            "status": Offer.Status.ACCEPTED,
            "current_turn": Offer.Turn.NONE
        }
    )

    # Check if pending contract exists
    contract = Contract.objects.filter(contract_number="AGRI-2026-RICE-002").first()
    if not contract:
        contract = Contract.objects.create(
            contract_number="AGRI-2026-RICE-002",
            offer=offer,
            farmer=farmer1,
            buyer=buyer1,
            crop_name=crop_rice.crop_name,
            variety=crop_rice.variety,
            quantity_kg=Decimal("2500"),
            agreed_price_per_kg=Decimal("88.00"),
            total_value=Decimal("220000.00"),
            delivery_location=offer.delivery_location,
            delivery_schedule=f"Fulfillment scheduled on or before {(date.today() + timedelta(days=20)).strftime('%d-%b-%Y')}.",
            quality_specifications=offer.quality_specifications,
            status=Contract.Status.PROPOSED,
            farmer_accepted=False,
            buyer_accepted=False
        )
        print(f"Created pending contract {contract.contract_number} (ID: {contract.id}) ready for signing!")
    else:
        # Reset to proposed for test signing
        contract.status = Contract.Status.PROPOSED
        contract.farmer_accepted = False
        contract.buyer_accepted = False
        contract.farmer_accepted_at = None
        contract.buyer_accepted_at = None
        contract.save()
        print(f"Reset contract {contract.contract_number} (ID: {contract.id}) to PROPOSED for test signing.")

    # Also ensure there is a pending payment on Contract 1 for buyer1 to test Razorpay
    c1 = Contract.objects.get(id=1)
    p_pending = Payment.objects.filter(contract=c1, status=Payment.Status.PENDING).first()
    if not p_pending:
        p_pending = Payment.objects.create(
            contract=c1,
            payer=buyer1,
            recipient=farmer1,
            amount=Decimal("45000.00"),
            payment_type=Payment.PaymentType.FINAL,
            status=Payment.Status.PENDING,
            notes="Milestone final settlement tranche for Contract #AGRI-2026-WHT-001"
        )
        print(f"Created pending Payment #{p_pending.id} for Razorpay checkout testing.")
    else:
        print(f"Pending Payment #{p_pending.id} exists for Razorpay checkout testing.")
