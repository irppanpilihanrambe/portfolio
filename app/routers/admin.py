from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models import AdminUser, Project, Contact
from app.schemas import LoginRequest, TokenResponse, AdminOut, DashboardStats
from app.auth import verify_password, create_access_token, get_current_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AdminUser).where(AdminUser.username == data.username)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=AdminOut)
async def get_me(current: AdminUser = Depends(get_current_admin)):
    return current


@router.get("/stats", response_model=DashboardStats)
async def get_stats(
    db: AsyncSession = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    total_projects  = await db.scalar(select(func.count(Project.id)))
    visible_projects = await db.scalar(
        select(func.count(Project.id)).where(Project.is_visible == True)
    )
    total_contacts  = await db.scalar(select(func.count(Contact.id)))
    unread_contacts = await db.scalar(
        select(func.count(Contact.id)).where(Contact.is_read == False)
    )

    return DashboardStats(
        total_projects=total_projects or 0,
        visible_projects=visible_projects or 0,
        total_contacts=total_contacts or 0,
        unread_contacts=unread_contacts or 0,
    )
