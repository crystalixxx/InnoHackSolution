from fastapi import HTTPException
from database import schemas, models
from core.security import get_password_hash
from sqlalchemy.orm import Session

import typing as t


def get_user_by_id(
        db: Session, user_id: int
) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)

    db_user = models.User(
        email=user.email,
        name=user.name,
        username=user.username,
        hashed_password=hashed_password,
        is_active=user.is_active,
        is_superuser=user.is_superuser
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(
        db: Session, skip: int = 0, limit: int = 100
) -> t.List[schemas.UserOut]:
    return db.query(models.User).offset(skip).limit(limit).all()


def delete_user(
        db: Session, user_id: int
) -> models.User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return user


def edit_user(
        db: Session, user_id: int, user: schemas.UserEdit
) -> models.User:
    db_user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_data = user.dict(exclude_unset=True)

    if "password" in new_data:
        new_data["hashed_password"] = get_password_hash(new_data["password"])
        del new_data["password"]

    for key, value in new_data:
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
