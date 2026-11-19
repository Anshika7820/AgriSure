import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.models import User, VerificationDocument
from contracts.models import Contract
from disputes.models import Dispute
from audit.models import AuditLog

# Seed pending verification documents
farmer2 = User.objects.filter(username="farmer2").first()
if farmer2 and not VerificationDocument.objects.filter(user=farmer2).exists():
    VerificationDocument.objects.create(
        user=farmer2,
        document_type="Revenue Land Record (Khasra-Khatauni / 7-12 Extract)",
        status=VerificationDocument.Status.PENDING,
        admin_notes=""
    )
    farmer2.is_verified = False
    farmer2.save(update_fields=["is_verified"])
    print("Created pending verification document for farmer2")

buyer2 = User.objects.filter(username="buyer2").first()
if buyer2 and not VerificationDocument.objects.filter(user=buyer2).exists():
    VerificationDocument.objects.create(
        user=buyer2,
        document_type="FSSAI Wholesale Manufacturing & Export License",
        status=VerificationDocument.Status.PENDING,
        admin_notes=""
    )
    buyer2.is_verified = False
    buyer2.save(update_fields=["is_verified"])
    print("Created pending verification document for buyer2")

# Seed a sample dispute case for admin arbitration
contract = Contract.objects.first()
farmer1 = User.objects.filter(username="farmer1").first()
buyer1 = User.objects.filter(username="buyer1").first()

if contract and not Dispute.objects.filter(contract=contract).exists():
    dispute = Dispute.objects.create(
        contract=contract,
        raised_by=buyer1,
        reason=Dispute.ReasonCategory.QUALITY,
        description="Batch moisture reading during pre-shipment quality inspection recorded 12.8%, which is slightly above the contractually stipulated 11.5% maximum threshold. Requesting joint sampling or platform quality re-testing.",
        status=Dispute.Status.OPEN
    )
    AuditLog.log("DISPUTE_RAISED", "Dispute", dispute.id, f"Buyer {buyer1.username} raised Quality dispute #{dispute.id} on Contract {contract.contract_number}", user=buyer1)
    print(f"Created sample Dispute #{dispute.id} on {contract.contract_number}")

print("Admin seed completed successfully.")
