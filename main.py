from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import init_db
from app.config import get_settings
from app.routers import projects, contacts, admin as admin_router

settings = get_settings()



@asynccontextmanager
async def lifespan(app: FastAPI):
    # await init_db()  <-- KASIH TANDA PAGAR DI DEPANNYA
    yield


app = FastAPI(
    title=settings.APP_TITLE,
    description="Portfolio API — FastAPI + PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Routers
app.include_router(projects.router)
app.include_router(contacts.router)
app.include_router(admin_router.router)


# ── Page Routes ───────────────────────────────────────────────

@app.get("/", include_in_schema=False)
async def landing(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": settings.APP_TITLE,
    })


@app.get("/admin", include_in_schema=False)
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "title": "Admin Panel | " + settings.APP_TITLE,
    })
    # Tambahkan ini di baris paling bawah agar dikenali Vercel
app = app
