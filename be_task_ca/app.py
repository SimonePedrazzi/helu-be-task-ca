from fastapi import FastAPI, Request, Response

from .database import SessionLocal
from .item.api import item_router
from .user.api import user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(item_router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get("/")
async def root():
    return {
        "message": "Thanks for shopping at Nile!"
    }  # the Nile is 250km longer than the Amazon
