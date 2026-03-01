# Customer Warning System

A Django + React system that allows staff to send customer warning emails (reminders, overdue notices, policy violations, etc.) via the **SendGrid** API.

---

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | Python 3.10+, Django 4.2, DRF     |
| Database  | SQLite (dev) / PostgreSQL (prod)  |
| Email     | SendGrid API                      |
| Frontend  | React 18 (optional staff dashboard) |

---

## Project Structure

```
email service/
├── manage.py
├── requirements.txt
├── .env.example
├── warning_system/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── warnings_app/            # Core Django app
│   ├── models.py            # Customer + WarningLog
│   ├── views.py             # REST API views
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # API URL routes
│   ├── admin.py             # Django Admin config
│   └── email_service.py     # SendGrid integration
└── frontend/                # React staff dashboard
    ├── package.json
    ├── public/
    └── src/
        ├── api.js
        ├── App.js
        └── components/
```

---

## Quick Start

### 1. Backend Setup

```bash
cd "email service"

# Create & activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
copy .env.example .env       # then edit .env with your values
```

Edit **`.env`** and set:
- `SECRET_KEY` — a random Django secret key
- `SENDGRID_API_KEY` — your SendGrid API key (starts with `SG.`)
- `DEFAULT_FROM_EMAIL` — verified sender email in SendGrid

```bash
# Run migrations & create a superuser
python manage.py migrate
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

The API is available at **http://127.0.0.1:8000/api/**.

Admin panel: **http://127.0.0.1:8000/admin/**.

### 2. Frontend Setup (Optional)

```bash
cd frontend
npm install
npm start
```

The React dashboard launches at **http://localhost:3000** and proxies API calls to Django.

> **Note:** You must be logged in (Django session auth) for API calls to succeed. Log in via the admin panel or API browser first.

---

## API Endpoints

| Method | URL                              | Description                       |
|--------|----------------------------------|-----------------------------------|
| GET    | `/api/customers/`                | List all customers (searchable)   |
| POST   | `/api/customers/`                | Create a customer                 |
| GET    | `/api/customers/{id}/`           | Retrieve a customer               |
| PUT    | `/api/customers/{id}/`           | Update a customer                 |
| DELETE | `/api/customers/{id}/`           | Delete a customer                 |
| GET    | `/api/customers/{id}/warnings/`  | List warnings for a customer      |
| GET    | `/api/warnings/`                 | List all warning logs (searchable)|
| GET    | `/api/warnings/{id}/`            | Retrieve a warning log            |
| POST   | `/api/send-warning/`             | **Send a warning email**          |
| GET    | `/api/warning-types/`            | List available warning types      |
| GET    | `/api/stats/`                    | Dashboard summary statistics      |

### Send Warning — Request Body

```json
{
  "customer_id": 1,
  "warning_type": "overdue",
  "subject": "Overdue Payment Notice",
  "message": "Your account is past due. Please remit payment immediately."
}
```

**Warning types:** `overdue`, `reminder`, `final_notice`, `policy_violation`, `general`

---

## Database Schema

### Customer
| Field       | Type         |
|-------------|--------------|
| id          | BigAutoField |
| first_name  | CharField    |
| last_name   | CharField    |
| email       | EmailField (unique) |
| phone       | CharField    |
| notes       | TextField    |
| created_at  | DateTime     |
| updated_at  | DateTime     |

### WarningLog
| Field              | Type                |
|--------------------|---------------------|
| id                 | BigAutoField        |
| customer           | FK → Customer       |
| warning_type       | CharField (choices)  |
| subject            | CharField           |
| message            | TextField           |
| status             | pending/sent/delivered/failed |
| sendgrid_message_id| CharField           |
| error_detail       | TextField           |
| sent_by            | CharField           |
| sent_at            | DateTime (nullable) |
| created_at         | DateTime            |

---

## SendGrid Setup

1. Create a free SendGrid account at https://sendgrid.com
2. Go to **Settings → API Keys** and create a key with **Mail Send** permission.
3. Under **Settings → Sender Authentication**, verify your sender email (or authenticate an entire domain with SPF/DKIM/DMARC).
4. Add the API key to your `.env` file.

---

## Production Notes

- Switch `DATABASES` in `settings.py` to PostgreSQL.
- Set `DEBUG=False` and configure `ALLOWED_HOSTS`.
- Use `gunicorn` or `daphne` instead of the development server.
- Run `python manage.py collectstatic` for serving static files.
- Consider adding token/JWT authentication for the API.
