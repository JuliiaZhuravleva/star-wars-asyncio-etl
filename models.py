import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, JSON

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')

PG_DSN = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5431/{POSTGRES_DB}'

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    __tablename__ = 'people'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    json: Mapped[dict] = mapped_column(JSON)


async def init_orm():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)