# 🌾 AgriSure — Assured Contract Farming System for Stable Market Access

<p align="center">
  <strong>Secure Contracts. Assured Markets. Better Farming.</strong>
</p>

<p align="center">
  A Digital Contract Farming Platform Connecting Farmers and Buyers
</p>

---

## 📌 About AgriSure

AgriSure is an enterprise-oriented, full-stack digital contract farming platform developed using **Python, Django, Django Channels, WebSockets, ReportLab, and Bootstrap 5**.

The platform aims to reduce agricultural market uncertainty by connecting farmers directly with food-processing companies, wholesale purchasers, and exporters.

It provides a centralized digital environment for crop listings, price negotiations, contract management, delivery tracking, payment records, and dispute resolution.

AgriSure focuses on building a transparent agricultural marketplace where farmers can access reliable buyers and buyers can procure agricultural produce through structured digital agreements.

---

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Platform Architecture](#-platform-architecture)
3. [Key Modules](#-key-modules)
4. [Technology Stack](#-technology-stack)
5. [User Roles](#-user-roles)
6. [Demo Credentials](#-demo-credentials)
7. [Project Structure](#-project-structure)
8. [Installation and Setup](#-installation-and-setup)
9. [Running the Application](#-running-the-application)
10. [Automated Testing](#-automated-testing)
11. [Production Deployment](#-production-deployment)
12. [Future Enhancements](#-future-enhancements)
13. [Disclaimer](#-disclaimer)
14. [Project Information](#-project-information)

---

## 🌱 Project Overview

Farmers often face challenges such as fluctuating market prices, uncertain demand, limited access to buyers, and delayed payments.

AgriSure addresses these challenges by providing a digital platform where farmers and buyers can establish transparent commercial agreements before agricultural produce is delivered.

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

### 💡 Why AgriSure?

| Traditional Farming Challenges | AgriSure Solution |
|---|---|
| Uncertain market prices | Structured price negotiation |
| Limited buyer connections | Digital agricultural marketplace |
| Lack of formal agreements | Digital contract management |
| Unclear delivery commitments | Delivery tracking |
| Payment transparency issues | Payment records and tracking |
| Difficult dispute management | Centralized dispute resolution |

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

AgriSure provides different functionalities according to user roles.

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

> **Security Note:** These are demonstration credentials, not guaranteed working accounts. Replace them with credentials generated by your setup process if necessary. Never use these passwords for a production deployment.

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

Make sure you have installed:

- Python 3.10 or later, compatible with your installed dependencies.
- pip
- Git
- A virtual environment
- PostgreSQL, if configured as the development database.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Anshika7820/AgriSure.git
```

Navigate into the project directory:

```bash
cd AgriSure
```

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

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install project dependencies:

```bash
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

**Important:** Do not commit your `.env` file or real credentials to GitHub.

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

For local development, an in-memory channel layer may be sufficient for basic testing.

For multi-process production deployments, configure a supported shared channel layer such as Redis.

Follow the project's ASGI configuration and dependency requirements when starting a WebSocket-capable server.

---

## 🧪 Automated Testing

Run the Django test suite:

```bash
python manage.py test
```

If the tests are organized in a specific Django application or test package, use the appropriate test label.

### Important Areas to Test

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

Before deploying AgriSure, configure the following components.

### 1. Database

Use PostgreSQL or another supported production database configured through environment variables.

### 2. Security

- Set `DEBUG=False`.
- Configure `ALLOWED_HOSTS`.
- Use a strong, secret Django key.
- Enable HTTPS and secure cookies.
- Protect private documents and uploaded files.
- Apply database migrations.
- Review authentication and authorization rules.

### 3. Static Files

Collect static files using:

```bash
python manage.py collectstatic --noinput
```

Configure the production web server or static-file storage to serve collected assets.

### 4. Real-Time Communication

Configure an ASGI-compatible deployment and Redis-backed channel layer if real-time WebSocket functionality is enabled.

### 5. Payments

Configure a supported payment gateway using server-side credentials and verified webhook handling.

Test payment workflows in sandbox mode before enabling live transactions.

---

## 🔮 Future Enhancements

Potential future improvements include:

- **Multilingual Support:** Introduce regional language support to make the platform accessible to more Indian farmers.
- **Agricultural Market Intelligence:** Integrate agricultural market-price data to improve pricing awareness.
- **Weather-Based Insights:** Provide weather-related information to support crop planning.
- **Mobile Application:** Develop mobile access for farmers and buyers.
- **Digital Document Verification:** Improve verification of farming agreements and supporting documents.
- **Advanced Analytics:** Introduce procurement and transaction analytics.
- **SMS Notifications:** Send alerts for important transactions and contractual updates.
- **Logistics Integration:** Improve delivery coordination and transportation tracking.

---

## ⚠️ Disclaimer

AgriSure is a digital contract farming project intended to support agricultural marketplace operations and transaction management.

The legal validity of electronic agreements depends on applicable laws and the implementation of appropriate acceptance and authentication mechanisms.

Payment tracking alone does not constitute escrow protection, and simulated payments must not be represented as real financial transactions.

Verify all security, legal, and payment integrations before using the platform for real commercial transactions.

---

## 🌾 Our Vision

We envision an agricultural ecosystem where farmers have better access to markets, buyers can procure agricultural produce through transparent agreements, and both parties can build reliable business relationships.

AgriSure aims to bring transparency, trust, and technology together to create a more structured and accessible contract farming ecosystem.

---

## 👩‍💻 Project Information

| Attribute | Details |
|---|---|
| **Project Name** | AgriSure |
| **Project Domain** | Agriculture Technology (AgriTech) |
| **Application Type** | Full-Stack Web Application |
| **Backend Framework** | Django |
| **Programming Language** | Python |
| **Primary Objective** | Improve transparency and market access in contract farming |
| **Version Control** | Git and GitHub |

---

<p align="center">
  <strong>AgriSure — Building stronger connections between farmers and buyers through technology.</strong>
  <br>
  🌾 Secure Contracts. Assured Markets. Better Farming.
</p>