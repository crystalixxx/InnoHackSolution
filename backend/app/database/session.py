from sqlmodel import Session
from .db import engine


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
