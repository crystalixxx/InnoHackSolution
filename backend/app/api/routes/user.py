from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.database.session import get_db
from app.core.auth import get_current_active_user, get_current_active_superuser
from app.database.schemas import UserCreate, UserEdit, User, UserOut
from app.database.crud.user import get_users


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