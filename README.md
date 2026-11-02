# 🌾 AgriSure — Assured Contract Farming System for Stable Market Access

**Secure Contracts. Assured Markets. Better Farming.**

AgriSure is an enterprise-oriented, full-stack digital contract farming platform developed using **Python, Django, Django Channels, WebSockets, ReportLab, and Bootstrap 5**.

The platform aims to reduce agricultural market uncertainty by connecting farmers directly with food-processing companies, wholesale purchasers, and exporters. It supports digital contract management, price negotiation, delivery tracking, payment records, and dispute resolution through a centralized web application.

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Platform Architecture](#-platform-architecture)
- [Key Modules](#-key-modules)
- [Technology Stack](#-technology-stack)
- [User Roles](#-user-roles)
- [Demo Credentials](#-demo-credentials)
- [Project Structure](#-project-structure)
- [Installation and Setup](#-installation-and-setup)
- [Running the Application](#-running-the-application)
- [Automated Testing](#-automated-testing)
- [Production Deployment](#-production-deployment)
- [Future Enhancements](#-future-enhancements)
- [Disclaimer](#-disclaimer)

---

## 🌱 Project Overview

Farmers often face challenges such as fluctuating market prices, uncertain demand, limited access to buyers, and delayed payments. AgriSure addresses these challenges by providing a digital platform where farmers and buyers can establish transparent commercial agreements before agricultural produce is delivered.

The platform facilitates the complete contract farming workflow, from crop listing and price negotiation to contract acceptance, delivery fulfillment, payment tracking, and dispute resolution.

### 🎯 Project Objectives

- Connect farmers directly with agricultural buyers.
- Improve market access and pricing transparency.
- Simplify crop discovery and procurement.
- Enable structured price and quantity negotiations.
- Maintain digital records of farming agreements.
- Track deliveries and contractual obligations.
- Improve transaction transparency and accountability.
- Provide role-based dashboards and transaction reports.

---

## 🏗️ Platform Architecture

The following diagram illustrates the intended application architecture.

```text
                         ┌───────────────────────────────┐
                         │       AgriSure Platform       │
                         │       Django Web App          │
                         └───────────────┬───────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
      ┌───────▼────────┐        ┌────────▼────────┐        ┌────────▼────────┐
      │  Farmer Portal │        │   Marketplace   │        │   Buyer Portal  │
      ├────────────────┤        ├─────────────────┤        ├─────────────────┤
      │ Farm Management│        │ Crop Listings   │        │ Procurement     │
      │ Crop Management│        │ Price Negotiation│       │ Offer Management│
      │ Offer Review   │        │ Real-time Chat  │        │ Contract Review │
      │ Delivery Update│        │ Search & Filters│        │ Delivery Tracking│
      └───────┬────────┘        └────────┬────────┘        └────────┬────────┘
              │                          │                          │
              └──────────────────────────┼──────────────────────────┘
                                         │
                         ┌───────────────▼───────────────┐
                         │    Contract Management        │
                         ├───────────────────────────────┤
                         │ Contract Proposals            │
                         │ Bilateral Acceptance          │
                         │ PDF Generation                │
                         │ Contract Amendments           │
                         └───────────────┬───────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
      ┌───────▼────────┐        ┌────────▼────────┐        ┌────────▼────────┐
      │ Delivery System│        │ Payment Records │        │ Notifications   │
      ├────────────────┤        ├─────────────────┤        ├─────────────────┤
      │ Dispatch       │        │ Payment Tracking│        │ WebSocket Events│
      │ Receipt        │        │ Transaction Logs│        │ User Alerts     │
      │ Quantity Check │        │ Receipts        │        │ Status Updates  │
      └────────────────┘        └─────────────────┘        └─────────────────┘
                                         │
                         ┌───────────────▼───────────────┐
                         │       Database Layer          │
                         │ PostgreSQL / SQLite           │
                         └───────────────────────────────┘
```

---

## 🚀 Key Modules

### 1. Authentication and Account Management

- User registration and login.
- Role-based accounts for farmers, buyers, and administrators.
- Profile management and password reset.
- Farmer and buyer verification workflows.
- Protected routes and permission checks.

### 2. Farm Management

- Register and manage multiple farms.
- Store farm location and area information.
- Associate crop listings with registered farms.
- Restrict farm management to authorized owners.

### 3. Crop Management and Marketplace

- Create, update, and manage crop listings.
- Display crop prices, quantities, quality details, and harvest dates.
- Search and filter crops by category, price, quantity, and location.
- Provide detailed crop information for interested buyers.

### 4. Offer Management and Price Negotiation

- Submit purchase offers.
- Propose counteroffers.
- Negotiate prices, quantities, and delivery schedules.
- Maintain negotiation history.
- Notify participants about offer status changes.

### 5. Digital Contract Management

- Create contract proposals from eligible accepted offers.
- Record acceptance by the relevant parties.
- Preserve agreed contract terms.
- Generate downloadable PDF contracts using ReportLab.
- Support contract amendments and status tracking.

### 6. Delivery and Fulfillment

- Schedule deliveries.
- Record dispatch and receipt details.
- Track delivery status.
- Record delivered and received quantities.
- Identify quantity discrepancies and delivery issues.

### 7. Payment Management

- Track payment obligations and transaction records.
- Maintain payment status and references.
- Support payment integration through a configured provider.
- Generate transaction receipts where implemented.
- Validate payment events on the server.

### 8. Real-Time Notifications

- Notify users about offers and counteroffers.
- Provide contract status updates.
- Deliver delivery and payment notifications.
- Use Django Channels and WebSockets where configured.
- Store notifications for later access.

### 9. Dispute Resolution

- Allow eligible users to raise disputes.
- Record dispute descriptions and supporting evidence.
- Track responses and resolution status.
- Provide authorized administrative review.

### 10. Ratings and Reviews

- Allow eligible parties to review completed transactions.
- Record ratings and feedback.
- Display reputation information where appropriate.
- Prevent duplicate reviews for the same eligible transaction.

### 11. Dashboards and Reports

- Provide separate dashboards for farmers, buyers, and administrators.
- Display transaction and contract summaries.
- Track crop listings, offers, deliveries, and payments.
- Generate reports from authorized database records.

### 12. Administration and Audit Logging

- Manage user verification.
- Monitor crop listings and contracts.
- Review disputes and transaction records.
- Record important administrative and business events.
- Restrict access to sensitive operational information.

---

## 💻 Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | Django |
| Frontend | HTML5, CSS3, JavaScript |
| UI Framework | Bootstrap 5 |
| Database | PostgreSQL / SQLite |
| Real-Time Communication | Django Channels, WebSockets |
| PDF Generation | ReportLab |
| Asynchronous Requests | Fetch API |
| Production Channel Layer | Redis |
| Version Control | Git and GitHub |

*The table describes the intended technology stack. Actual dependencies and integrations depend on the implementation in the repository.*

---

## 👥 User Roles

| Role | Responsibilities |
|---|---|
| **Farmer** | Manage farms and crops, review offers, negotiate prices, manage contracts, and track deliveries and payments. |
| **Buyer** | Browse crops, submit offers, negotiate terms, manage procurement contracts, and track transactions. |
| **Administrator** | Manage verification, monitor platform activities, review disputes, and oversee authorized administrative operations. |

---

## 🔑 Demo Credentials

Use the following credentials only if these demonstration accounts have been created in your local database.

| Role | Username | Password | Purpose |
|---|---|---|---|
| Administrator | `admin` | `admin@123` | Platform administration |
| Farmer | `farmer1` | `farmer@123` | Farm and crop management |
| Farmer | `farmer2` | `farmer@123` | Crop listings and offers |
| Buyer | `buyer1` | `buyer@123` | Procurement and contracts |
| Buyer | `buyer2` | `buyer@123` | Marketplace and transactions |

> **Security note:** These are demonstration credentials, not guaranteed working accounts. Replace them with credentials generated by your setup process if necessary. Never use these passwords for a production deployment.

---

## 📁 Project Structure

The following is a suggested modular project structure. Adjust it to match the actual files in your repository.

```text
AgriSure/
│
├── manage.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
├── farms/
├── marketplace/
├── negotiations/
├── contracts/
├── deliveries/
├── payments/
├── notifications/
├── disputes/
├── reviews/
├── reports/
├── audit/
│
├── templates/
│   ├── base.html
│   ├── accounts/
│   ├── marketplace/
│   ├── contracts/
│   └── dashboards/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
└── tests/
```

---

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### Prerequisites

- Python 3.10 or later, compatible with your installed dependencies.
- pip
- Git
- A virtual environment
- PostgreSQL, if configured as the development database.

### Step 1: Clone the Repository

```bash
git clone <your-github-repository-url>
cd AgriSure
```

Replace `<your-github-repository-url>` with your repository's clone URL.

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a local `.env` file using `.env.example` as a reference.

Configure the required values, such as:

```text
DJANGO_SECRET_KEY=replace-with-a-secure-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

Add database, email, Redis, and payment gateway settings if your implementation requires them.

**Do not commit your `.env` file or real credentials to GitHub.**

### Step 5: Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

If migrations are already included in the repository, applying `migrate` may be sufficient.

### Step 6: Create an Administrator

```bash
python manage.py createsuperuser
```

Follow the prompts to create your administrator account.

### Step 7: Load Demonstration Data

If the repository includes a working seed script, run:

```bash
python seed_data.py
```

If no seed script exists, create users and sample records through the application or Django administration interface.

---

## ▶️ Running the Application

<<<<<<< HEAD
Start the Django development server:

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

For Django administration, visit:

```text
http://127.0.0.1:8000/admin/
```

Use the administrator credentials you created during setup.

### Running Real-Time Features

If the project uses Django Channels, configure its channel layer according to your development settings.

For local development, an in-memory channel layer may be sufficient for basic testing. For multi-process production deployments, configure a supported shared channel layer such as Redis.

Follow the project's ASGI configuration and dependency requirements when starting a WebSocket-capable server.

---

## 🧪 Automated Testing

Run the Django test suite:

```bash
python manage.py test
```

If the tests are organized in a specific Django application or test package, use the appropriate test label.

Important areas to test include:

- Registration and authentication.
- Role-based permissions.
- Farm and crop management.
- Marketplace search and filtering.
- Offer submission and negotiation.
- Contract creation and acceptance.
- Delivery tracking.
- Payment validation.
- Notifications.
- Dispute management.

Run and verify the tests before describing a feature as fully implemented.

---

## 🚀 Production Deployment

Before deploying AgriSure, configure the following:

### Database

Use PostgreSQL or another supported production database configured through environment variables.

### Security

- Set `DEBUG=False`.
- Configure `ALLOWED_HOSTS`.
- Use a strong, secret Django key.
- Enable HTTPS and secure cookies.
- Protect private documents and uploaded files.
- Apply database migrations.
- Review authentication and authorization rules.

### Static Files

```bash
python manage.py collectstatic --noinput
```

Configure the production web server or static-file storage to serve collected assets.

### Real-Time Communication

Configure an ASGI-compatible deployment and Redis-backed channel layer if real-time WebSocket functionality is enabled.

### Payments

Configure a supported payment gateway using server-side credentials and verified webhook handling. Test payment workflows in sandbox mode before enabling live transactions.

---

## 🔮 Future Enhancements

Potential future improvements include:

- Multilingual support for Indian farmers.
- Integration with agricultural market-price data.
- Weather-based crop planning insights.
- Mobile application support.
- Secure digital document verification.
- Advanced procurement analytics.
- SMS alerts for important transactions.
- Improved delivery and logistics integration.

---

## ⚠️ Disclaimer

AgriSure is a digital contract farming project intended to support agricultural marketplace operations and transaction management.

The legal validity of electronic agreements depends on applicable laws and the implementation of appropriate acceptance and authentication mechanisms. Payment tracking alone does not constitute escrow protection, and simulated payments must not be represented as real financial transactions.

Verify all security, legal, and payment integrations before using the platform for real commercial transactions.

---

## 👩‍💻 Project Information

**Project Name:** AgriSure  
**Project Domain:** Agriculture Technology (AgriTech)  
**Application Type:** Full-Stack Web Application  
**Backend Framework:** Django  
**Primary Objective:** Improve transparency and market access in contract farming.

---

**AgriSure — Building stronger connections between farmers and buyers through technology.** 🌾
=======
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
 #   A g r i S u r e  
 #   A g r i S u r e  
 
>>>>>>> 0047ad8 (first commit)
#   A g r i S u r e  
 