from fastapi import FastAPI
from sqlmodel import SQLModel

from api.main import api_router
from database.db import engine

import uvicorn

app = FastAPI()

app.include_router(api_router, prefix="")


if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
