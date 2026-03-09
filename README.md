# Customer Warning System — In-App Messaging Platform

A self-contained Django + React messaging platform for sending customer warnings and notices. Staff send messages (overdue notices, reminders, policy violations, etc.) to customers who read them within the app — like a lightweight Gmail clone. **No external email APIs or third-party services required.**

---

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | Python 3.10+, Django 4.2, DRF     |
| Database  | SQLite (dev) / PostgreSQL (prod)  |
| Auth      | Django session authentication      |
| Frontend  | React 18                          |

---

## How It Works

1. **Customers register** an account through the app.
2. **Staff log in** and send warning messages to customers (choosing a warning type, subject, and body).
3. **Customers log in** and see their inbox — unread messages are highlighted.
4. Opening a message automatically marks it as **read** with a timestamp.
5. Staff see a **dashboard** with stats (total customers, messages, read/unread counts, breakdown by type).

---

## Project Structure

```
email service/
├── manage.py
├── requirements.txt
├── .env.example               # Template for environment variables
├── .env                       # Your local config (git-ignored)
├── .gitignore
├── db.sqlite3                 # SQLite dev database (git-ignored)
├── warning_system/            # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── warnings_app/              # Core Django app
│   ├── models.py              # User (custom) + Message models
│   ├── views.py               # REST API views
│   ├── serializers.py         # DRF serializers
│   ├── urls.py                # API URL routes
│   └── admin.py               # Django Admin config
└── frontend/                  # React app
    ├── package.json
    ├── public/
    └── src/
        ├── api.js             # Axios API client + CSRF handling
        ├── App.js             # Root component (auth flow + routing)
        ├── index.js
        ├── index.css          # Global styles
        └── components/
            ├── Login.js       # Login form
            ├── Register.js    # Customer registration form
            ├── Dashboard.js   # Staff stats overview
            ├── Customers.js   # Customer list (staff)
            ├── Inbox.js       # Message inbox (customer & staff)
            ├── MessageView.js # Full message detail view
            └── SendWarning.js # Send message form (staff)
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
- `DEBUG` — `True` for development

```bash
# Run migrations & create a staff superuser
python manage.py migrate
python manage.py createsuperuser
```

> After creating the superuser, set their role to "staff" via the Django admin or shell:
> ```bash
> python manage.py shell -c "from warnings_app.models import User; u=User.objects.get(username='admin'); u.role='staff'; u.save()"
> ```

```bash
# Start the development server
python manage.py runserver
```

The API is available at **http://127.0.0.1:8000/api/**.  
Admin panel: **http://127.0.0.1:8000/admin/**.

### 2. Frontend Setup

```bash
cd frontend
npm install
npm start
```

The React app launches at **http://localhost:3000** and proxies API calls to Django.

---

## User Roles

| Role       | Capabilities                                              |
|------------|-----------------------------------------------------------|
| **staff**  | Dashboard, customer list, send warnings, view sent messages |
| **customer** | Register, log in, view inbox, read messages              |

---

## API Endpoints

| Method | URL                       | Auth      | Description                         |
|--------|---------------------------|-----------|-------------------------------------|
| POST   | `/api/auth/register/`     | Public    | Register a new customer account     |
| POST   | `/api/auth/login/`        | Public    | Log in (returns user data + session)|
| POST   | `/api/auth/logout/`       | Required  | Log out                             |
| GET    | `/api/auth/me/`           | Required  | Get current user                    |
| GET    | `/api/customers/`         | Staff     | List customers (searchable)         |
| GET    | `/api/inbox/`             | Required  | Customer: received / Staff: sent    |
| GET    | `/api/messages/{id}/`     | Required  | View message detail (auto-marks read)|
| POST   | `/api/send-message/`      | Staff     | Send a warning to a customer        |
| GET    | `/api/warning-types/`     | Required  | List available warning types        |
| GET    | `/api/stats/`             | Staff     | Dashboard statistics                |

### Send Message — Request Body

```json
{
  "recipient_id": 1,
  "warning_type": "overdue",
  "subject": "Overdue Payment Notice",
  "body": "Your account is past due. Please remit payment immediately."
}
```

**Warning types:** `overdue`, `reminder`, `final_notice`, `policy_violation`, `general`

---

## Database Schema

### User (extends AbstractUser)
| Field       | Type              |
|-------------|-------------------|
| id          | BigAutoField      |
| username    | CharField (unique)|
| email       | EmailField        |
| first_name  | CharField         |
| last_name   | CharField         |
| phone       | CharField         |
| role        | staff / customer  |
| date_joined | DateTime          |

### Message
| Field        | Type               |
|--------------|--------------------|
| id           | BigAutoField       |
| sender       | FK → User (staff)  |
| recipient    | FK → User (customer)|
| warning_type | CharField (choices) |
| subject      | CharField          |
| body         | TextField          |
| is_read      | BooleanField       |
| read_at      | DateTime (nullable)|
| created_at   | DateTime           |

---

## Default Test Account

A staff admin account is pre-created:
- **Username:** `admin`
- **Password:** `admin123`

Register additional customer accounts through the app's registration page.

---

## Production Notes

- Switch `DATABASES` in `settings.py` to PostgreSQL.
- Set `DEBUG=False` and configure `ALLOWED_HOSTS`.
- Use `gunicorn` or `daphne` instead of the development server.
- Run `python manage.py collectstatic` for serving static files.
- Set a strong, unique `SECRET_KEY`.
- Consider adding rate limiting to registration and login endpoints.
