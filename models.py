from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer

import os


POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "12341")
POSTGRES_DB = os.getenv("POSTGRES_DB", "netology_asyncio")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")


POSTGRES_DSN = (
    f"postgresql+asyncpg://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

engine = create_async_engine(POSTGRES_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Character(Base):

    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(1000))
    eye_color: Mapped[str] = mapped_column(String(1000))
    films: Mapped[str] = mapped_column(String(1000))
    gender: Mapped[str] = mapped_column(String(1000))
    hair_color: Mapped[str] = mapped_column(String(1000))
    height: Mapped[str] = mapped_column(String(1000))
    homeworld: Mapped[str] = mapped_column(String(1000))
    mass: Mapped[str] = mapped_column(String(1000))
    name: Mapped[str] = mapped_column(String(1000))
    skin_color: Mapped[str] = mapped_column(String(1000))
    species: Mapped[str] = mapped_column(String(1000))
    starships: Mapped[str] = mapped_column(String(1000))
    vehicles: Mapped[str] = mapped_column(String(1000))


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()