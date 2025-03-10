from typing import Annotated
from datetime import datetime
from enum import Enum

from sqlalchemy import String, Text, CheckConstraint, ForeignKey, text, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from uuid import UUID

from database.database import Base

int_id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_64 = Annotated[str, mapped_column(String(64), nullable=False)]
created_at= Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at= Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.utcnow
    )]



class User(Base):
    __tablename__ = "users"

    id: Mapped[int_id]
    username: Mapped[str_64]
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    authorized: Mapped[bool]= mapped_column(default=False)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    __table_args__ = (
        CheckConstraint("email LIKE '%@%.%'", name="valid_email"),
    )

    tasks = relationship("Todolist", back_populates="user")

class Todolist(Base):
    __tablename__ = "todolist"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)
    is_done: Mapped[bool] = mapped_column(default=False)

    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="tasks")


class CalendarTask(Base):
    __tablename__ = "calendar_tasks"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text)
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    finish_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    notify_before: Mapped[int]

    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    __table_args__ = (
        CheckConstraint("notify_before >= 0 AND notify_before <= 60", name="valid_NotifyBefore"),
    )