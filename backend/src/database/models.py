from typing import Annotated
from datetime import datetime
from enum import Enum

from sqlalchemy import String, Text, CheckConstraint, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

from database.database import Base

int_id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_16 = Annotated[str, mapped_column(String(16), nullable=False)]
created_at= Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at= Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now() + interval '1 day')"),
    onupdate=datetime.utcnow
    )]



class User(Base):
    __tablename__ = "users"

    id: Mapped[int_id]
    first_name: Mapped[str_16]
    last_name: Mapped[str_16]
    age: Mapped[int]
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    authorized: Mapped[bool]= mapped_column(default=True)
    admin: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]



    __table_args__ = (
        CheckConstraint("email LIKE '%@%.%'", name="valid_email"), 
        CheckConstraint("age > 0 AND age <= 100", name="valid_age"),
    )

class Todolist(Base):
    __tablename__ = "todolist"

    id: Mapped[int_id]
    description: Mapped[str] = mapped_column(Text)
    is_done: Mapped[bool] = mapped_column(default=False)

    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

class CalendarTask(Base):
    __tablename__ = "calendar_tasks"

    id: Mapped[int_id]
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text)
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    finish_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    notify_before: Mapped[int]

    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    __table_args__ = (
        CheckConstraint("notify_before >= 0 AND notify_before <= 60", name="valid_NotifyBefore"),
    )