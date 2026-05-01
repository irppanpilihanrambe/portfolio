from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
from datetime import datetime


# ── Project ───────────────────────────────────────────────────

class ProjectBase(BaseModel):
    title:       str
    category:    str
    description: str
    tech_stack:  List[str] = []
    order_index: int = 0
    is_visible:  bool = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title:       Optional[str] = None
    category:    Optional[str] = None
    description: Optional[str] = None
    tech_stack:  Optional[List[str]] = None
    order_index: Optional[int] = None
    is_visible:  Optional[bool] = None


class ProjectOut(ProjectBase):
    id:         int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Contact ───────────────────────────────────────────────────

class ContactCreate(BaseModel):
    name:    str
    email:   EmailStr
    subject: str
    message: str

    @field_validator("name", "subject", "message")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty")
        return v.strip()


class ContactOut(BaseModel):
    id:         int
    name:       str
    email:      str
    subject:    str
    message:    str
    is_read:    bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Auth ──────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"


class AdminOut(BaseModel):
    id:       int
    username: str
    email:    str

    model_config = {"from_attributes": True}


# ── Stats ─────────────────────────────────────────────────────

class DashboardStats(BaseModel):
    total_projects:  int
    visible_projects: int
    total_contacts:  int
    unread_contacts: int
