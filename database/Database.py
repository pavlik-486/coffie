from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE = "sqlite+aiosqlite:///./database.db"
engine = create_async_engine(DATABASE, echo=True)
session = async_sessionmaker(bind=engine, expire_on_commit=False)
Base = declarative_base()

