# 🚀 Portfolio Full-Stack App

**FastAPI + PostgreSQL + Premium Frontend + Admin Panel**

---

## 📁 Project Structure

```
portfolio/
├── main.py                    # FastAPI app entry point
├── create_admin.py            # One-time admin seeder
├── requirements.txt
├── .env.example               # → copy to .env and fill in
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
├── app/
│   ├── config.py              # Settings (reads from .env)
│   ├── database.py            # Async SQLAlchemy engine
│   ├── models.py              # DB models: Project, Contact, AdminUser
│   ├── schemas.py             # Pydantic request/response schemas
│   ├── auth.py                # JWT authentication
│   ├── routers/
│   │   ├── projects.py        # GET/POST/PUT/DELETE /api/projects
│   │   ├── contacts.py        # POST /api/contacts (public) + admin CRUD
│   │   └── admin.py           # /api/admin/login, /me, /stats
│   └── utils/
│       └── email.py           # Async SMTP email sender
├── static/                    # CSS / JS / images (if any)
└── templates/
    ├── index.html             # 🌐 Public landing page (premium)
    └── admin.html             # 🔐 Admin panel (projects + inbox)
```

---

## ⚙️ Setup & Run

### 1. Clone & enter project
```bash
cd portfolio
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
```
Edit `.env` — fill in your PostgreSQL credentials and SMTP settings:
```
DATABASE_URL=postgresql+asyncpg://postgres:yourpassword@localhost:5432/portfolio_db
SECRET_KEY=your-random-secret-key-min-32-chars
ADMIN_USERNAME=admin
ADMIN_PASSWORD=YourSecurePassword!
SMTP_USER=your@gmail.com
SMTP_PASSWORD=your-gmail-app-password
CONTACT_RECEIVER_EMAIL=your@gmail.com
```

### 5. Create PostgreSQL database
```bash
createdb portfolio_db
# or via psql:
psql -U postgres -c "CREATE DATABASE portfolio_db;"
```

### 6. Create admin + seed sample projects
```bash
python create_admin.py
```

### 7. Run the server
```bash
uvicorn main:app --reload --port 8000
```

---

## 🌐 URLs

| URL | Description |
|-----|-------------|
| `http://localhost:8000/` | Public landing page |
| `http://localhost:8000/admin` | Admin panel (login required) |
| `http://localhost:8000/docs` | Interactive API docs (Swagger UI) |
| `http://localhost:8000/redoc` | ReDoc API docs |

---

## 🔐 Admin Panel Features

- **Login** with username/password → JWT token stored in localStorage
- **Dashboard** — Stats: total projects, visible, total messages, unread
- **Projects** — Add / Edit / Delete / Show-Hide projects
- **Inbox** — View messages, mark as read, delete

---

## 📡 API Endpoints

### Public
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects/` | List visible projects |
| POST | `/api/contacts/` | Submit contact form |

### Admin (requires Bearer token)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/admin/login` | Login → get token |
| GET | `/api/admin/me` | Current admin info |
| GET | `/api/admin/stats` | Dashboard statistics |
| GET | `/api/projects/admin/all` | All projects (incl. hidden) |
| POST | `/api/projects/` | Create project |
| PUT | `/api/projects/{id}` | Update project |
| DELETE | `/api/projects/{id}` | Delete project |
| GET | `/api/contacts/` | List all messages |
| PATCH | `/api/contacts/{id}/read` | Mark as read |
| DELETE | `/api/contacts/{id}` | Delete message |

---

## 📧 Gmail SMTP Setup

1. Enable 2-Factor Authentication on Gmail
2. Go to Google Account → Security → App Passwords
3. Create an App Password for "Mail"
4. Use that 16-character password as `SMTP_PASSWORD` in `.env`

---

## 🎨 Customization

### Change your profile info
Edit `templates/index.html`:
- Replace `Your Name` with your real name (3 places)
- Replace the Unsplash photo URL with your actual photo
- Edit the `hero-bio` paragraph with your summary

### Add/edit projects
Use the Admin Panel at `/admin` — no code editing needed!

---

## 🚀 Production Deployment

```bash
# Use gunicorn with uvicorn workers
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

For production:
- Set `SECRET_KEY` to a long random string
- Use a proper PostgreSQL instance (not localhost)
- Put behind **Nginx** as reverse proxy
- Use **HTTPS** (Let's Encrypt / Certbot)
