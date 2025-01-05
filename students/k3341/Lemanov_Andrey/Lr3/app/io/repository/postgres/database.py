from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from students.k3341.Lemanov_Andrey.Lr3.app.config.config import config
from students.k3341.Lemanov_Andrey.Lr3.app.io.repository.postgres.models.models import Base

engine = create_async_engine(config.database.DATABASE_URL, echo=False, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        return session
