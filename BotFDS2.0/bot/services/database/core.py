from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import Config

config = Config()
engine = create_async_engine(config.DB_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def create_db():
    from services.database.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)