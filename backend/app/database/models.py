import uuid

from typing import Optional
from datetime import datetime, timezone
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    email: EmailStr = Field(unique=True, index=True, nullable=False)
    name: str = Field(nullable=False)
    username: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    created_tasks: list["Task"] = Relationship(back_populates="author")
    created_projects: list["Project"] = Relationship(back_populates="author")

class TagAndTask(SQLModel, table=True):
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    task_id: Optional[int] = Field(default=None, foreign_key="task.id", primary_key=True)

class Task(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: str = Field(nullable=False)
    description: Optional[str] = Field(nullable=True)

    deadline: Optional[datetime] = Field(default=None, nullable=True)
    urgency: Optional[int] = Field(default=None, nullable=True)

    status_id: Optional[int] = Field(default=None, foreign_key="status.id")
    status: Optional["Status"] = Relationship(back_populates="status")

    author_id: Optional[int] = Field(default=None, foreign_key="user.id")
    author: Optional["User"] = Relationship(back_populates="created_tasks")

    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=True)

    reviewer_id: Optional[int] = Field(default=None, foreign_key="user.id")
    reviewer: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Task.reviewer_id]"})

    executor_id: Optional[int] = Field(default=None, foreign_key="user.id")
    executor: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Task.executor_id]"})

    project_id: Optional[int] = Field(default=None, foreign_key="project.id")
    project: Optional["Project"] = Relationship(back_populates="applied_tasks")

    tags: list["Tag"] = Relationship(back_populates="tasks", link_model=TagAndTask)


class TagAndProject(SQLModel, table=True):
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)
    project_id: int | None = Field(default=None, foreign_key="project.id", primary_key=True)


class Project(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: str = Field(nullable=False)
    description: str | None = Field(nullable=True)

    author_id: int | None = Field(default=None, foreign_key="user.id")
    author: User | None = Relationship(back_populates='project')

    status_id: int | None = Field(default=None, foreign_key="status.id")
    status: Optional["Status"] = Relationship(back_populates='projects')

    tags: list["Tag"] = Relationship(back_populates='projects', link_model=TagAndProject)

    applied_tasks: list["Task"] = Relationship(back_populates="project")


class Status(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: str = Field(nullable=False)

    projects: list["Project"] = Relationship(back_populates="status")


class Tag(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: str = Field(nullable=False)

    tasks: list["Tag"] = Relationship(back_populates="tags", link_model=TagAndTask)
    projects: list["Tag"] = Relationship(back_populates='tags', link_model=TagAndProject)
