import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config.config import settings

database_url = os.environ.get('DATABASE_URL_asyncpg')

async_engine = create_async_engine(
    url=database_url,
    echo=True,
)

async_session = async_sessionmaker(async_engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    db = async_session()
    try:
        yield db
    finally: 
        await db.aclose()
