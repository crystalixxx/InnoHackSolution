import os

# os.environ["DATABASE_URL"] = 'postgresql://admin:admin@localhost:5432/postgres'

SQLMODEL_DATABASE_URI = os.getenv("DATABASE_URL")
print(SQLMODEL_DATABASE_URI)
