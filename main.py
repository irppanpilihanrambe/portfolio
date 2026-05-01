import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# IMPORT INI SESUAI STRUKTUR PROJECT KAMU

from app.routers import projects, contacts, admin_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@asynccontextmanager
async def lifespan(app: FastAPI):
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
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)

# Routers
app.include_router(projects.router)
app.include_router(contacts.router)
app.include_router(admin_router.router)


@app.get("/", include_in_schema=False)
async def landing(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": settings.APP_TITLE,
        },
    )


@app.get("/admin", include_in_schema=False)
async def admin_page(request: Request):
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "title": "Admin Panel | " + settings.APP_TITLE,
        },
    )


handler = app