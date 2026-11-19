import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import Client
from accounts.models import User, VerificationDocument
from farms.models import Farm
from marketplace.models import CropCategory, CropListing
from negotiations.models import Offer
from contracts.models import Contract
from deliveries.models import Delivery
from payments.models import Payment
from disputes.models import Dispute

client = Client()

passed = 0
failed = 0
results = []

def test(name, status_or_bool, expected=200):
    global passed, failed
    if isinstance(status_or_bool, bool):
        ok = status_or_bool
        code = "PASS" if ok else "FAIL"
    else:
        code = status_or_bool
        ok = (code == expected or (isinstance(expected, (list, tuple)) and code in expected))
    if ok:
        passed += 1
        print(f"  [PASS] {name} (code: {code})")
        results.append((name, "PASS", code))
    else:
        failed += 1
        print(f"  [FAIL] {name} (got {code}, expected {expected})")
        results.append((name, "FAIL", code))

print("=" * 65)
print("COMPREHENSIVE WEBSITE FEATURE & BUTTON VERIFICATION")
print("=" * 65)

# --- 1. ANONYMOUS ACCESS ---
print("\n=== [1] Testing Anonymous Routes & Auth Gateways ===")
test("Home Page", client.get("/").status_code)
test("Marketplace Catalog", client.get("/marketplace/").status_code)
crop = CropListing.objects.first()
test("Crop Detail Anonymous", client.get(f"/marketplace/crop/{crop.id}/").status_code)
test("Login Page", client.get("/login/").status_code)
test("Register Farmer Page", client.get("/register/farmer/").status_code)
test("Register Buyer Page", client.get("/register/buyer/").status_code)
test("Protected Dashboard Redirects to Login", client.get("/dashboard/").status_code, 302)

# --- 2. FARMER PORTAL ---
print("\n=== [2] Testing Farmer User Flow (farmer1) ===")
client.login(username="farmer1", password="farmer@123")
farmer = User.objects.get(username="farmer1")
farm = Farm.objects.filter(farmer=farmer).first()

test("Farmer Dashboard Redirect", client.get("/dashboard/").status_code, 302)
test("Farmer Dashboard Direct", client.get("/marketplace/farmer/dashboard/").status_code)
test("Farms List", client.get("/farms/").status_code)
test("Farm Detail", client.get(f"/farms/{farm.id}/").status_code)
test("Farm Edit Page", client.get(f"/farms/{farm.id}/edit/").status_code)
test("Farm Add Page", client.get("/farms/add/").status_code)
test("My Crops List", client.get("/marketplace/farmer/crops/").status_code)
test("Add Crop Page", client.get("/marketplace/farmer/crops/add/").status_code)
farmer_crop = CropListing.objects.filter(farmer=farmer).first()
if farmer_crop:
    test("Edit Crop Page", client.get(f"/marketplace/farmer/crops/{farmer_crop.id}/edit/").status_code)
    test("Crop Status Toggle (POST)", client.post(f"/marketplace/farmer/crops/{farmer_crop.id}/toggle-status/", {"status": "ACTIVE"}).status_code, 302)
test("Farmer Offers List", client.get("/negotiations/farmer/offers/").status_code)
test("Contracts List", client.get("/contracts/").status_code)
farmer_contract = Contract.objects.filter(farmer=farmer).first()
if farmer_contract:
    test("Contract Detail View", client.get(f"/contracts/{farmer_contract.id}/").status_code)
    test("Contract PDF Generation", client.get(f"/contracts/{farmer_contract.id}/pdf/").status_code)
test("Deliveries List", client.get("/deliveries/").status_code)
farmer_delivery = Delivery.objects.filter(contract__farmer=farmer).first()
if farmer_delivery:
    test("Delivery Detail View", client.get(f"/deliveries/{farmer_delivery.id}/").status_code)
test("Payments List", client.get("/payments/").status_code)
farmer_payment = Payment.objects.filter(recipient=farmer).first()
if farmer_payment:
    test("Payment Detail View", client.get(f"/payments/{farmer_payment.id}/").status_code)
farmer_paid = Payment.objects.filter(recipient=farmer, status=Payment.Status.SUCCESS).first()
if farmer_paid:
    test("Payment Receipt Download (Success TXN)", client.get(f"/payments/{farmer_paid.id}/receipt/").status_code)
test("Farmer Reports Page", client.get("/reports/farmer/").status_code)
test("User Profile View", client.get("/profile/").status_code)
test("User Profile Edit Page", client.get("/profile/edit/").status_code)
test("Verification Upload Page", client.get("/profile/verify/").status_code)
test("Notifications List", client.get("/notifications/").status_code)
test("Notifications API Unread", client.get("/notifications/api/unread/").status_code)
client.logout()

# --- 3. BUYER PORTAL ---
print("\n=== [3] Testing Buyer User Flow (buyer1) ===")
client.login(username="buyer1", password="buyer@123")
buyer = User.objects.get(username="buyer1")

test("Buyer Dashboard Redirect", client.get("/dashboard/").status_code, 302)
test("Buyer Dashboard Direct", client.get("/negotiations/buyer/dashboard/").status_code)
test("Buyer Offers List", client.get("/negotiations/buyer/offers/").status_code)
test("Marketplace Browse", client.get("/marketplace/").status_code)
test("Marketplace Search & Filter", client.get("/marketplace/?q=Wheat&sort_by=-created_at").status_code)
buyer_offer = Offer.objects.filter(buyer=buyer).first()
if buyer_offer:
    test("Negotiation Thread View", client.get(f"/negotiations/offers/{buyer_offer.id}/").status_code)
test("Buyer Contracts List", client.get("/contracts/").status_code)
buyer_contract = Contract.objects.filter(buyer=buyer).first()
if buyer_contract:
    test("Buyer Contract Detail", client.get(f"/contracts/{buyer_contract.id}/").status_code)
    test("Buyer Contract PDF", client.get(f"/contracts/{buyer_contract.id}/pdf/").status_code)
test("Buyer Deliveries List", client.get("/deliveries/").status_code)
test("Buyer Payments List", client.get("/payments/").status_code)
buyer_payment = Payment.objects.filter(payer=buyer).first()
if buyer_payment:
    test("Buyer Payment Detail", client.get(f"/payments/{buyer_payment.id}/").status_code)
    test("Buyer Payment Receipt", client.get(f"/payments/{buyer_payment.id}/receipt/").status_code)
test("Buyer Disputes List", client.get("/disputes/").status_code)
test("Buyer Reports Page", client.get("/reports/buyer/").status_code)
test("Buyer Profile View", client.get("/profile/").status_code)
client.logout()

# --- 4. ADMIN GOVERNANCE PORTAL ---
print("\n=== [4] Testing Administrator Operations (admin) ===")
client.login(username="admin", password="admin@123")

test("Admin Dashboard Redirect", client.get("/dashboard/").status_code, 302)
test("Admin Dashboard Direct", client.get("/admin-dashboard/").status_code)
test("Admin Verifications List", client.get("/admin-dashboard/verifications/").status_code)
v_doc = VerificationDocument.objects.first()
if v_doc:
    test("Admin Verification Action (POST)", client.post(f"/admin-dashboard/verifications/{v_doc.id}/action/", {"action": "APPROVE"}).status_code, 302)
test("Admin Users List", client.get("/admin-dashboard/users/").status_code)
test("Admin Audit Logs", client.get("/admin-dashboard/audit-logs/").status_code)
test("Admin Reports Analytics", client.get("/reports/admin-reports/").status_code)
test("Admin Disputes List", client.get("/disputes/").status_code)
admin_dispute = Dispute.objects.first()
if admin_dispute:
    test("Admin Dispute Detail View", client.get(f"/disputes/{admin_dispute.id}/").status_code)
test("Admin Django Native Backend", client.get("/admin/").status_code)
client.logout()

print("\n" + "=" * 65)
print(f"VERIFICATION SUMMARY: {passed} PASSED, {failed} FAILED (TOTAL: {passed + failed})")
print("=" * 65)
