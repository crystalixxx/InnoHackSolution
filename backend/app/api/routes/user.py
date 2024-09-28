from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.database.session import get_db
from app.core.auth import get_current_active_user, get_current_active_superuser
from app.database.schemas import UserCreate, UserEdit, User, UserOut
from app.database.crud.user import get_users, create_user, edit_user, delete_user, get_user_by_id

users_routers = APIRouter()


@users_routers.get(
    "/users",
    response_model=t.List[User],
    response_model_exclude_none=True
)
async def users_list(
        response: Response,
        db=Depends(get_db),
        current_user=Depends(get_current_active_user),
):
    users = get_users(db)
    return users


@users_routers.get(
    "/users/{user_id}",
    response_model=User,
    response_model_exclude_none=True
)
async def users_get_by_id(
        response: Response,
        user_id: int,
        db=Depends(get_db),
        current_user=Depends(get_current_active_user)
):
    return get_user_by_id(db, user_id)


@users_routers.get(
    "/users/me",
    response_model=User,
    response_model_exclude_none=True
)
async def users_me(
        response: Response,
        db=Depends(get_db),
        current_user=Depends(get_current_active_user)
):
    return current_user


@users_routers.post(
    "/users"
)
async def user_creation(
        response: Response,
        user: UserCreate,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    return create_user(db, user)


@users_routers.put(
    "/users/{user_id}",
    response_model=User,
    response_model_exclude_none=True
)
async def user_edit(
        response: Response,
        user_id: int,
        user: UserEdit,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    return edit_user(db, user_id, user)


@users_routers.delete(
    "/users/{user_id}",
    response_model=User,
    response_model_exclude_none=True
)
async def user_delete(
        response: Response,
        user_id: int,
        db=Depends(get_db),
        current_user=Depends(get_current_active_superuser),
):
    return delete_user(db, user_id)
