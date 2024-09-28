from sqlmodel import Session, select

from database.models import User
from database.schemas import UserCreate
from core.security import get_password_hash


def get_user_by_email(db: Session, email: str) -> User | None:
    return None


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        name=user.name,
        username=user.username,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
