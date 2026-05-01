from sqlalchemy import (
    Column, Integer, String, Text, Boolean,
    DateTime, ARRAY, func
)
from app.database import Base


class Project(Base):
    __tablename__ = "projects"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(200), nullable=False)
    category    = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    tech_stack  = Column(ARRAY(String), nullable=False, default=[])
    order_index = Column(Integer, default=0)
    is_visible  = Column(Boolean, default=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())


class Contact(Base):
    __tablename__ = "contacts"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(150), nullable=False)
    email      = Column(String(255), nullable=False)
    subject    = Column(String(300), nullable=False)
    message    = Column(Text, nullable=False)
    is_read    = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AdminUser(Base):
    __tablename__ = "admin_users"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String(100), unique=True, nullable=False, index=True)
    email           = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active       = Column(Boolean, default=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
