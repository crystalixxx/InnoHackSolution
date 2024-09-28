from sqlmodel import create_engine, SQLModel

from app.core import config

path = config.SQLMODEL_DATABASE_URI

engine = create_engine(path)
