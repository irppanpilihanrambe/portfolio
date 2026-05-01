from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models import Contact, AdminUser
from app.schemas import ContactCreate, ContactOut
from app.auth import get_current_admin
from app.utils.email import send_contact_email

router = APIRouter(prefix="/api/contacts", tags=["Contacts"])


# ── Public ────────────────────────────────────────────────────

@router.post("/", response_model=ContactOut, status_code=status.HTTP_201_CREATED)
async def submit_contact(
    data: ContactCreate,
    db: AsyncSession = Depends(get_db),
):
    contact = Contact(**data.model_dump())
    db.add(contact)
    await db.flush()
    await db.refresh(contact)

    # Send email notification (non-blocking — failure won't break response)
    await send_contact_email(
        name=data.name,
        email=data.email,
        subject=data.subject,
        message=data.message,
    )

    return contact


# ── Admin ─────────────────────────────────────────────────────

@router.get("/", response_model=List[ContactOut])
async def list_contacts(
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    result = await db.execute(
        select(Contact).order_by(Contact.created_at.desc())
    )
    return result.scalars().all()


@router.patch("/{contact_id}/read", response_model=ContactOut)
async def mark_read(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact.is_read = True
    await db.flush()
    await db.refresh(contact)
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    await db.delete(contact)
