from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from asyncpg.exceptions import UniqueViolationError

from aiohttp import web

from models import ORM_MODEL_CLS, ORM_MODEL
from mapping import raise_http_error

from logger import py_logger


async def select_filter_item(session: AsyncSession, model_cls: ORM_MODEL_CLS, 
                             item_value: str) -> ORM_MODEL:
    py_logger.info(f"SQL: select_filter // {model_cls.__name__} // {item_value}")
    query = select(model_cls).where(model_cls.email == item_value)
    result = await session.execute(query)
    item = result.scalar()
    if item is False:
        py_logger.error(f"{model_cls.__name__} not found")
        raise raise_http_error(web.HTTPNotFound, f"{model_cls.__name__} not found")
    return item


async def select_item(session: AsyncSession, model_cls: ORM_MODEL_CLS, item_id: Union[int, str]) -> ORM_MODEL:
    py_logger.info(f"SQL: select // {model_cls.__name__} // {item_id}")
    item = await session.get(model_cls, item_id)
    if item is None:
        py_logger.error(f"{model_cls.__name__} not found")
        raise raise_http_error(web.HTTPNotFound, f"{model_cls.__name__} not found")
    
    return item


async def insert_item(session: AsyncSession, model_cls: ORM_MODEL_CLS, commit: bool = True, **params) -> ORM_MODEL:
    py_logger.info(f"SQL: insert // {model_cls.__name__} // {params}")
    new_item = model_cls(**params)
    session.add(new_item)
    if commit:
        try:
            await session.commit()
        except IntegrityError:
            py_logger.error(f"such {model_cls.__tablename__.lower()} already exists")
            raise raise_http_error(web.HTTPConflict, f"such {model_cls.__name__.lower()} already exists")
    return new_item


async def update_item(session: AsyncSession, item: ORM_MODEL, commit: bool = True, **params) -> ORM_MODEL:
    py_logger.info(f"SQL: update // {item} // {params}")
    for field, value in params.items():
        setattr(item, field, value)
    session.add(item)
    if commit:
        try:
            await session.commit()
        except IntegrityError:
            py_logger.error(f"such {item.__tablename__.lower()} already exists")
            raise raise_http_error(web.HTTPConflict, f"such {item.__name__.lower()} already exists")
            ...
    return item


async def delete_item(session: AsyncSession, item: ORM_MODEL, commit: bool = True):
    py_logger.info(f"SQL: delete // {item}")
    await session.delete(item)
    if commit:
        await session.commit()