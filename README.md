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

# Installation & Setup (Docker-based)

This project uses **Docker** and **Docker Compose** to run all services (web, database, cache, broker, workers, and reverse proxy). No need to install Python, PostgreSQL, Redis, or RabbitMQ on your host machine.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

---

## Quick Start (with Docker Compose)

### 1. Clone the project
```bash
git clone <repository-url>
cd A
```

### 2. Environment variables
Copy the example environment file and fill it with your own values:
```bash
cp .env.example .env
```
> **Important:** For production, set `DEBUG=False` and use strong passwords for `POSTGRES_PASSWORD`, `RABBITMQ_PASSWORD`, etc.

### 3. Build and start all services
```bash
docker compose up -d --build
```
This will start:
- **web**: Django + Gunicorn (port 8000, exposed via Nginx)
- **db**: PostgreSQL
- **redis**: Cache & session store
- **rabbitmq**: Celery broker
- **celery-worker**: Celery worker for async tasks
- **celery-beat**: Celery Beat for scheduled tasks
- **nginx**: Reverse proxy (port 80)

### 4. Apply database migrations
```bash
docker compose exec web python manage.py migrate
```

### 5. Collect static files
```bash
docker compose exec web python manage.py collectstatic --noinput
```

### 6. Create a superuser (admin)
```bash
docker compose exec web python manage.py createsuperuser
```

### 7. Access the application
- Open `http://localhost` in your browser.
- Admin panel: `http://localhost/admin`

---

## Development mode (live reload)

If you want to see code changes without restarting containers, you can run the development server inside the container:

```bash
# Stop the production web service
docker compose stop web

# Run Django's runserver with live reload
docker compose run --service-ports web python manage.py runserver 0.0.0.0:8000
```

Now changes to Python, HTML, and static files will be applied immediately.  
To go back to production mode, just run `docker compose start web`.

---

## Useful commands

| Task | Command |
|------|---------|
| Start all services | `docker compose up -d` |
| Stop all services | `docker compose down` |
| Restart a specific service | `docker compose restart web` |
| View logs (all services) | `docker compose logs -f` |
| View logs for a specific service | `docker compose logs -f web` |
| Run Django management commands | `docker compose exec web python manage.py <command>` |
| Run Celery commands (if needed) | `docker compose exec celery-worker celery -A A <command>` |

---

## Production deployment

For production, make sure your `.env` contains:
- `DEBUG=False`
- `ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com`
- Strong passwords for all secrets
- Real credentials for third-party services (Arvan, Zarinpal, Email, etc.)

Then on your VPS, just run:
```bash
docker compose up -d --build
```

---

## (Optional) Running without Docker

If you prefer to run everything locally without Docker, you will need to install and configure:
- Python 3.12 + virtualenv
- PostgreSQL
- Redis
- RabbitMQ
- Celery

Then follow the classic Django setup (see the legacy instructions in the repository history). However, **Docker is the recommended and supported way** for both development and production.

---

## 🔑 Environment Variables

This project uses environment variables for all sensitive and configuration settings.

A template file named `.env.example` is provided in the project root. To get started:

```bash
cp .env.example .env
```

Then open `.env` and fill in all the required values (API keys, passwords, database credentials, etc.).

> ⚠️ **Important:** The `.env` file contains secrets and should **never** be committed to version control. It is already ignored via `.gitignore`.

For a complete list of available variables, refer to the `.env.example` file itself — it includes comments explaining each setting.

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
│   ├── tasks.py                 # Upload/download/delete file tasks
│   └── templatetags/extra_tags.py  # Custom filters and tags
│
├── utils.py                   # Shared utilities (IsAdminMixin)
├── aws/                        # Files downloaded from the bucket (local)
└── manage.py
├── bucket.py               # Object storage management
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

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for more details.
