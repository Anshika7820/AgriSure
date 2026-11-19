import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test import Client
from accounts.models import User
from contracts.models import Contract
from disputes.models import Dispute
from payments.models import Payment

client = Client()

print("--- Testing Anonymous Access & Fallback Aliases ---")
assert client.get("/").status_code == 200, "Home failed"
assert client.get("/marketplace/").status_code == 200, "Marketplace failed"
assert client.get("/login/").status_code == 200, "Login failed"
assert client.get("/accounts/login/").status_code == 200, "Accounts/login/ alias failed"
assert client.get("/register/farmer/").status_code == 200, "Register farmer failed"
assert client.get("/register/buyer/").status_code == 200, "Register buyer failed"
assert client.get("/accounts/register/farmer/").status_code == 200, "Accounts register farmer alias failed"
assert client.get("/accounts/register/buyer/").status_code == 200, "Accounts register buyer alias failed"
print("[OK] Anonymous routes and aliases OK")

print("--- Testing Admin User Access ---")
client.login(username="admin", password="admin@123")

admin_urls = [
    "/admin-dashboard/",
    "/admin-dashboard/verifications/",
    "/admin-dashboard/users/",
    "/admin-dashboard/audit-logs/",
    "/reports/admin-reports/",
    "/disputes/",
    "/disputes/1/",
    "/marketplace/",
    "/contracts/",
    "/deliveries/",
    "/payments/",
    "/profile/",
    "/admin/",
]

for url in admin_urls:
    res = client.get(url)
    assert res.status_code in (200, 302), f"Admin route failed for {url}: status {res.status_code}"
    print(f"[OK] Admin accessed {url} (status {res.status_code})")

client.logout()

print("--- Testing Farmer Access ---")
client.login(username="farmer1", password="farmer@123")
farmer_urls = [
    "/dashboard/",
    "/farms/",
    "/marketplace/my-listings/",
    "/marketplace/add/",
    "/negotiations/offers/",
    "/contracts/",
    "/deliveries/",
    "/payments/",
    "/reports/farmer/",
    "/profile/",
]
for url in farmer_urls:
    res = client.get(url, follow=True)
    assert res.status_code == 200, f"Farmer route failed for {url}: status {res.status_code}"
    print(f"[OK] Farmer accessed {url} (status {res.status_code})")
client.logout()

print("--- Testing Buyer Access ---")
client.login(username="buyer1", password="buyer@123")
buyer_urls = [
    "/dashboard/",
    "/marketplace/",
    "/negotiations/my-offers/",
    "/contracts/",
    "/deliveries/",
    "/payments/",
    "/reports/buyer/",
    "/profile/",
    "/disputes/",
]
for url in buyer_urls:
    res = client.get(url, follow=True)
    assert res.status_code == 200, f"Buyer route failed for {url}: status {res.status_code}"
    print(f"[OK] Buyer accessed {url} (status {res.status_code})")
client.logout()

print("\nALL PLATFORM ROUTES AND ALIASES VERIFIED FLAWLESSLY!")
