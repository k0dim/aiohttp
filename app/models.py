from typing import Type

from cachetools import cached
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer, func
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import EmailType
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID


from config import DNS

Base = declarative_base()

class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(24), nullable=False)
    surename = Column(String(32), nullable=False)
    email = Column(EmailType, nullable=False, unique=True, index=True)
    password = Column(String(60), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Token(Base):

    __tablename__ = "token"

    id = Column(UUID, server_default=func.uuid_generate_v4(), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", lazy="joined")


class Ads(Base):

    __tablename__ = "adc"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", lazy="joined")


@cached({})
def get_engine():
    return create_async_engine(DNS)


@cached({})
def get_session_maker():
    return sessionmaker(bind=get_engine(), class_=AsyncSession, expire_on_commit=False)


async def init_models():
    async with create_async_engine(DNS).begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    await create_async_engine(DNS).dispose()



ORM_MODEL_CLS = Type[User] | Type[Token] | Type[Ads]
ORM_MODEL = User | Token | Ads