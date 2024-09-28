from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

tag_task_table = Table(
    'tag_task',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True),
    Column('task_id', Integer, ForeignKey('task.id'), primary_key=True)
)

tag_project_table = Table(
    'tag_project',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True),
    Column('project_id', Integer, ForeignKey('project.id'), primary_key=True)
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=True)
    urgency = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="tasks")

    status_id = Column(Integer, ForeignKey('status.id'))
    status = relationship("Status", back_populates="tasks")

    project_id = Column(Integer, ForeignKey('project.id'))
    project = relationship("Project", back_populates="tasks")

    tags = relationship("Tag", secondary=tag_task_table, back_populates="tasks")


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="projects")

    status_id = Column(Integer, ForeignKey('status.id'))
    status = relationship("Status", back_populates="projects")

    tasks = relationship("Task", back_populates="project")
    tags = relationship("Tag", secondary=tag_project_table, back_populates="projects")


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="status")
    projects = relationship("Project", back_populates="status")


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    tasks = relationship("Task", secondary=tag_task_table, back_populates="tags")
    projects = relationship("Project", secondary=tag_project_table, back_populates="tags")
