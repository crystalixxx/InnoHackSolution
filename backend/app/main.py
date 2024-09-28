from fastapi import FastAPI

from api.main import api_router

import uvicorn

app = FastAPI(
    title="InnoHack", docs_url="/api/docs", openapi_url="/api"
)

app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
