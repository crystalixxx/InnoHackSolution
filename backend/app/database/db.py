from sqlmodel import create_engine, SQLModel

path = 'postgresql://localhost:admin@postgres:5432/localhost'

engine = create_engine(path)
