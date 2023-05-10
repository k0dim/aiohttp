import asyncio

from aiohttp import web

from views import login, UserView, AdView
from middleware import session_middleware, auth_middleware
from models import init_models, close_db, get_session_maker

from logger import py_logger


async def app_context(app: web.Application):
    py_logger.info("Start App")
    Session = get_session_maker()
    async with Session() as session:
        await session.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
        await session.commit()
    await init_models()
    py_logger.info("Start DB")
    yield
    await close_db()
    py_logger.info("Finish DB")
    py_logger.info("Finish App")


async def get_app():
    app = web.Application(middlewares=[session_middleware])
    app_auth_required_user = web.Application(middlewares=[session_middleware, auth_middleware])
    app_auth_required_ads = web.Application(middlewares=[session_middleware, auth_middleware])

    app.cleanup_ctx.append(app_context)
    app.add_routes(
        [
            web.post("/login", login),
            web.post("/users/", UserView),
        ]
    )

    app_auth_required_user.add_routes(
        [
            web.get("/{user_id:\d+}", UserView),
            web.patch("/{user_id:\d+}", UserView),
            web.delete("/{user_id:\d+}", UserView),
        ]
    )

    app_auth_required_ads.add_routes(
        [
            web.post("/create_ad/", AdView),
            web.get("/{ad_id:\d+}", AdView),
            web.patch("/{ad_id:\d+}", AdView),
            web.delete("/{ad_id:\d+}", AdView),
        ]
    )

    app.add_subapp(prefix="/users", subapp=app_auth_required_user)
    app.add_subapp(prefix="/ads", subapp=app_auth_required_ads)

    return app