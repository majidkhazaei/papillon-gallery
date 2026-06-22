# 🛍️ PapillonArtGallery — Django E-Commerce Platform

A full-featured e-commerce project built with Django. This project implements a custom authentication system, product management, session-based cart, ZarinPal payment gateway, coupon system, secure file uploads, Redis caching, and many other features of a real-world online store.

---

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation & Setup](#-installation--setup)
- [Environment Variables](#-environment-variables)
- [Project Structure](#-project-structure)
- [Architecture & Technical Decisions](#-architecture--technical-decisions)
- [Management Commands](#-management-commands)
- [Future Roadmap](#-future-roadmap)

---

## ✨ Features

### 🔐 Authentication & Users
- Custom user model (`AbstractBaseUser` + `PermissionsMixin`) with phone-number-based login
- Two-step registration with OTP (one-time password) verification sent via SMS (Kavenegar)
- Password reset via email (SMTP / Gmail App Password)
- Group and permission management with fine-grained control in the admin panel
- Secure avatar upload with content validation, resizing, and image reprocessing

### 🛒 Products & Categories
- Nested categories (self-referencing `ForeignKey`) for subcategory support
- Many-to-many relationship between products and categories (`ManyToManyField`)
- Rich-text product descriptions (CKEditor)
- Product filtering by category with dedicated category URLs

### 🛍️ Cart & Orders
- Session-based shopping cart (no database writes before checkout)
- Cart item count and total displayed site-wide via a Context Processor
- Final order placement, converting the session cart into database records (`Order` and `OrderItem`)
- Coupon discount system with date-range and active-status validation

### 💳 Payments
- ZarinPal payment gateway integration
- Two-step transaction verification (Request + Verify) for payment security

### ☁️ Infrastructure & Advanced Tooling
- Asynchronous task processing (Celery + RabbitMQ) for SMS sending, file download, and file deletion
- Cloud object storage on Arvan Cloud (S3-compatible)
- Custom management commands for cleaning up expired OTP codes
- Custom template filters and tags (Persian-formatted prices, Jalali dates, inclusion tags)
- Automatic sitemap generation for SEO
- Customized admin panel (branding, custom action buttons, read-only fields)
- Structured logging with a rotating file handler
- Caching and session management with Redis
- Production-ready PostgreSQL database

---

## ⚙️ Requirements

| Tool | Recommended Version |
|---|---|
| Python | 3.11+ |
| PostgreSQL | 14+ |
| Redis | 6+ |
| RabbitMQ | 3.x |
| pip | latest |

---

## 🚀 Installation & Setup

```bash
# 1. Clone the project
git clone <repository-url>
cd A

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up the .env file (see section below)
cp .env.example .env

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create a superuser
python manage.py createsuperuser

# 7. Run the development server
python manage.py runserver
```

### Running the Celery worker (in a separate terminal)

```bash
celery -A A worker -l info
```

### Running Redis and RabbitMQ (if not installed system-wide)

```bash
docker run -d -p 6379:6379 redis
docker run -d -p 5672:5672 rabbitmq
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root with the following values:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# PostgreSQL
DB_NAME=galleryshop
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=127.0.0.1
DB_PORT=5432

# Email (Gmail App Password)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Arvan Cloud Object Storage
ARVAN_ACCESS_KEY=your-access-key
ARVAN_SECRET_KEY=your-secret-key
ARVAN_ENDPOINT=https://your-endpoint.arvancloud.com
ARVAN_BUCKET=your-bucket-name

# ZarinPal
ZP_MERCHANT_ID=your-merchant-id

# Kavenegar (SMS)
KAVENEGAR_API_KEY=your-api-key
```

> ⚠️ The `.env` file should never be committed — make sure it's listed in `.gitignore`.

---

## 📁 Project Structure

```
A/
├── A/                      # Core project settings
│   ├── settings.py
│   ├── urls.py
│   └── celery_conf.py      # Celery configuration
│
├── accounts/                # Authentication and users
│   ├── models.py            # User, OtpCode, Avatar, Coupon
│   ├── managers.py          # UserManager
│   ├── validators.py        # Avatar upload validation
│   ├── tasks.py             # Celery tasks (OTP sending)
│   └── management/commands/ # Custom management commands
│       └── remove_expired_otps.py
│
├── products/                 # Products and categories
│   ├── models.py             # Category, Product
│   └── sitemap.py            # SEO sitemap
│
├── orders/                   # Cart and orders
│   ├── cart.py                # Cart management class (session-based)
│   ├── models.py               # Order, OrderItem, Coupon
│   └── context_processors.py  # Site-wide cart access
│
├── home/                      # Homepage and cloud bucket
│   ├── bucket.py               # Object storage management
│   ├── tasks.py                 # Upload/download/delete file tasks
│   └── templatetags/extra_tags.py  # Custom filters and tags
│
├── utils.py                   # Shared utilities (IsAdminMixin)
├── aws/                        # Files downloaded from the bucket (local)
└── manage.py
```

---

## 🏗️ Architecture & Technical Decisions

### Layered cloud operations
`View → Tasks → Bucket` — each layer only talks to the layer directly below it. If the storage provider ever changes, only `bucket.py` needs to be updated.

### Session-based shopping cart
The cart is deliberately not stored in the database to avoid creating abandoned, half-finished order records. It's only converted into a real `Order` record at the moment of checkout.

### Async processing with Celery
Slow or non-critical operations (SMS sending, file upload/download) are offloaded to Celery so the user-facing response isn't blocked.


### Two-step payment verification
An order's `paid` status only changes after the transaction is re-verified with ZarinPal (not simply because the user was redirected back from the gateway), preventing manual/forged payment confirmation.

---

## 🛠️ Management Commands

```bash
# Remove expired OTP codes
python manage.py remove_expired_otps
```

> 💡 It's recommended to run this command on a schedule (e.g., every 5 minutes) using Celery Beat.

---

## 🗺️ Future Roadmap

- [ ] Add Celery Beat for scheduled command execution
- [ ] Unit and integration tests (pytest / Django TestCase)
- [ ] Sales reporting dashboard
- [ ] Support for multiple payment methods

---

## 📄 License

This project was built for personal learning purposes.
