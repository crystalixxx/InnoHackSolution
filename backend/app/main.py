from fastapi import FastAPI, Request
from database.models import User, Project, Task
from sqlmodel import select, Session, create_engine
from typing import Optional, List
from fastapi.responses import JSONResponse
from core.auth import get_current_user

engine = create_engine('postgresql://admin:admin@postgres:5432/postgres')

from api.main import api_router

import uvicorn

app = FastAPI(
    title="InnoHack", docs_url="/api/docs", openapi_url="/api"
)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
