# AgriSure — Assured Contract Farming System for Stable Market Access

AgriSure is an enterprise-grade, real-time, full-stack digital contract farming platform developed with **Python, Django, Django Channels, WebSockets, ReportLab, and Bootstrap 5**.

The system addresses price volatility and agricultural market uncertainty by connecting farmers directly with food-processing companies, wholesale purchasers, and exporters through legally enforceable, bilaterally signed digital contracts, delivery weighbridge tracking, and secure escrow payment settlement.

---

## 🌾 Platform Architecture & Key Modules

```
                    ┌──────────────────────────────────────────────┐
                    │            AgriSure Web Application          │
                    └──────────────────────┬───────────────────────┘
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │                                 │                                 │
┌────────▼────────┐              ┌────────▼────────┐              ┌────────▼────────┐
│ Farmer Portal   │              │ Marketplace &   │              │ Buyer Portal    │
│ Farm Land Mgmt  │              │ Negotiation Hub │              │ Procurement Hub │
│ Crop Listings   │              │ Real-time Chat  │              │ Deal Tracking   │
│ Offer Review    │              │ Bilateral Terms │              │ Escrow Checkout │
└────────┬────────┘              └────────┬────────┘              └────────┬────────┘
         │                                │                                │
         └────────────────────────────────┼────────────────────────────────┘
                                          │
                    ┌─────────────────────▼──────────────────────┐
                    │   Digital Contract Engine (ReportLab PDF)   │
                    │   - Bilateral Cryptographic Signatures      │
                    │   - Fulfillment Schedules & Deliveries      │
                    │   - Dispute Resolution Tribunal             │
                    │   - Verified Escrow Milestone Settlements   │
                    └────────────────────────────────────────────┘
```

---

## 🚀 Key Modules Built

1. **Authentication & Accounts**:
   - Custom User model with roles: `FARMER`, `BUYER`, `ADMIN`.
   - Role-specific onboarding with land records for farmers and GSTIN/CIN for buyers.
   - KYC Verification Documents workflow with admin approval.

2. **Farm Management**:
   - Multiple farm plot registrations per farmer (area in acres, soil classification, irrigation source, Khasra/survey number).
   - Strict ownership protection ensuring crops can only be assigned to the farmer's registered land.

3. **Crop Management & Marketplace**:
   - Search, filter by category, state, price range, harvest date, and available volume.
   - Dynamic real-time commercial pricing calculator.
   - Comprehensive detail page with farmer credibility ratings and direct offer action.

4. **Bilateral Price Negotiation**:
   - Complete negotiation audit log with counter-proposals on volume, rate, and delivery dates.
   - Real-time notification updates and discussion threads.
   - Bilateral acceptance locks remaining stock atomically and prepares a structured digital contract.

5. **Contract Lifecycle & PDF Generation**:
   - Complete state machine: `DRAFT` ➔ `PROPOSED` ➔ `ACCEPTED` ➔ `ACTIVE` ➔ `COMPLETED` (or `DISPUTED` / `CANCELLED`).
   - Bilateral authenticated electronic signatures with SHA-256 hashes and UTC timestamps.
   - Automated PDF contract formulation with embedded branding, legal terms, and signature certificates using ReportLab.
   - Formal Contract Amendment workflow for climate-driven schedule or yield adjustments.

6. **Delivery & Logistics Fulfillment**:
   - Consignment dispatch slips recorded by farmers (vehicle registration, driver phone).
   - Post-arrival weighbridge scale confirmation by buyers with quality acceptance or rejection records.
   - Automatic contract completion once total contracted volume is confirmed.

7. **Escrow Payments & Milestone Settlements**:
   - 15% Advance booking deposit upon contract activation.
   - 85% Milestone settlement generated upon weighbridge scale verification.
   - Interactive checkout gateway simulator (UPI QR, NetBanking, Escrow, Corporate Card) with cryptographic HMAC-SHA256 signature verification.
   - Downloadable official tax invoice / settlement voucher receipts in PDF.

8. **Real-time Infrastructure**:
   - Django Channels & WebSockets (`ws/notifications/` and `ws/negotiations/<offer_id>/`).
   - In-memory channel layer for instant local setup + Redis-ready for production.
   - Transparent polling fallback ensures zero disruption even on restrictive networks.

9. **Dispute Conciliation Tribunal**:
   - Formal grievance escalation freezing milestone payouts until platform mediator ruling.
   - Documented resolution notes and contract restoration.

10. **Reviews & Reputation**:
    - Bilateral 1–5 star ratings and reviews unlocked exclusively upon verified contract fulfillment.

11. **Platform Operations & Audit Logging**:
    - Dedicated Admin Governance Dashboard for document KYC reviews, user suspension, and comprehensive audit trails.

---

## 🔑 Demo Credentials

| Role | Username | Password | Profile / Focus |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin@123` | Platform Compliance & Grievance Arbitration |
| **Farmer** | `farmer1` | `farmer@123` | Gurpreet Singh (Golden Fields Agri, Punjab - Wheat & Basmati) |
| **Farmer** | `farmer2` | `farmer@123` | Ramesh Patel (Organic Cotton & Groundnut, Gujarat) |
| **Buyer** | `buyer1` | `buyer@123` | Apex Agri Foods Pvt. Ltd. (Food Processing Company) |
| **Buyer** | `buyer2` | `buyer@123` | National Grain & Spice Exports Ltd. (Agri-Exporter) |

---

## 🛠️ Local Setup & Running Instructions

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.13)
- pip

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed Platform Demonstration Data
```bash
python seed_data.py
```

### 5. Run Automated Tests
```bash
python manage.py test tests
```

### 6. Start the Real-Time Server
```bash
python manage.py runserver 127.0.0.1:8000
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 📄 Production Deployment Guidelines

1. **PostgreSQL**: Configure `DATABASES` with environment variables (`DATABASE_URL`).
2. **Channel Layer**: Configure Redis backend in `CHANNEL_LAYERS` in `config/settings.py`:
   ```python
   CHANNEL_LAYERS = {
       "default": {
           "BACKEND": "channels_redis.core.RedisChannelLayer",
           "CONFIG": {"hosts": [os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/1")]},
       }
   }
   ```
3. **ASGI Server**: Run using Daphne or Uvicorn:
   ```bash
   daphne -b 0.0.0.0 -p 8000 config.asgi:application
   ```
4. **Static Collection**:
   ```bash
   python manage.py collectstatic --noinput
   ```
#   A g r i S u r e  
 