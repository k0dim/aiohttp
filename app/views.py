from aiohttp import web

from crud import select_item, select_filter_item, \
                insert_item, update_item, delete_item
from mapping import raise_http_error, raise_http_succeed
from auth import hash_password, check_password, check_owner
from models import User, Token, Ads

from logger import py_logger


async def login(request: web.Request):
    login_data = await request.json()
    user = await select_filter_item(request["session"], User, login_data["email"])
    
    if not user or not check_password(login_data["password"], user.password):
        raise_http_error(web.HTTPUnauthorized, "incorrect login or password")
        py_logger.error("incorrect login or password")

    token = Token(user=user)
    request["session"].add(token)
    await request["session"].commit()

    py_logger.info(f"/login - body")

    message = {
        "token": str(token.id)
    }
    return raise_http_succeed(web.HTTPOk, message=message)


class UserView(web.View):

    async def get(self):
        user_id = int(self.request.match_info["user_id"])
        user = await select_item(self.request["session"], User, user_id)
        py_logger.info(f"/users/{user_id}")

        message = {
            "id": user.id,
            "name": user.name,
            "surename": user.surename,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }
        return raise_http_succeed(web.HTTPOk, message=message)

    
    async def post(self):
        user_data = await self.request.json()
        user_data["password"] = hash_password(user_data["password"])
        new_user = await insert_item(self.request["session"], User, **user_data)
        py_logger.info(f"/user/ - body")

        message = {
            "state": "create",
            "data": {
                "id": new_user.id,
                "email": new_user.email,
            }
        }
        return raise_http_succeed(web.HTTPCreated, message=message)

    
    async def patch(self):
        user_id = int(self.request.match_info["user_id"])
        check_owner(self.request, user_id)
        user_data = await self.request.json()

        if "password" in user_data:
            user_data["password"] = hash_password(user_data["password"])

        user = await select_item(self.request["session"], User, user_id)
        update_user = await update_item(self.request["session"], user, **user_data)
        py_logger.info(f"/users/{user_id} - body")

        message = {
            "state": "update",
            "data": {
                "id": update_user.id,
                "email": update_user.email,
                "created_at": update_user.created_at.isoformat()
            }
        }
        return raise_http_succeed(web.HTTPOk, message=message)

        
    async def delete(self):
        user_id = int(self.request.match_info["user_id"])
        check_owner(self.request, user_id)
        user = await select_item(self.request["session"], User, user_id)
        await delete_item(self.request["session"], user)
        py_logger.info(f"/users/{user_id}")

        return raise_http_succeed(web.HTTPNoContent, message=None)


class AdView(web.View):

    async def get(self):
        ad_id = int(self.request.match_info["ad_id"])
        ad = await select_item(self.request["session"], Ads, ad_id)
        user = await select_item(self.request["session"], User, int(ad.user_id))
        py_logger.info(f"/ads/{ad_id}")

        message = {
            "id": ad.id,
            "title":ad.title,
            "description": ad.description,
            "user":{
                    "id": user.id,
                    "name": user.name,
                    "surename": user.surename,
                    "email": user.email,
                    "created_at": user.created_at.isoformat()
            },
            "created_at": ad.created_at.isoformat()
        }
        return raise_http_succeed(web.HTTPOk, message=message)
    
    
    async def post(self):
        ad_data = await self.request.json()
        token = await select_item(self.request["session"], Token, self.request.headers.get("Token"))
        ad_data["user_id"] = token.user_id
        new_ad = await insert_item(self.request["session"], Ads, **ad_data)
        py_logger.info(f"/ads/ - body {ad_data}")

        message = {
            "state": "create",
            "data": {
                "id": new_ad.id,
                "title":new_ad.title,
                "description": new_ad.description,
                "user_id":new_ad.user_id
            }
        }
        return raise_http_succeed(web.HTTPCreated, message=message)
    
    
    async def patch(self):
        ad_id = int(self.request.match_info["ad_id"])
        ad = await select_item(self.request["session"], Ads, ad_id)
        check_owner(self.request, int(ad.user_id))

        ad_data = await self.request.json()
        update_ad = await update_item(self.request["session"], ad, **ad_data)
        py_logger.info(f"/ads/{ad_id} - body {ad_data}")
        
        message = {
            "state": "update",
            "data": {
                "id": update_ad.id,
                "title":update_ad.title,
                "description": update_ad.description,
                "user_id":update_ad.user_id,
                "created_at": update_ad.created_at.isoformat()
            }
        }
        return raise_http_succeed(web.HTTPOk, message=message)
    
        
    async def delete(self):
        ad_id = int(self.request.match_info["ad_id"])
        ad = await select_item(self.request["session"], Ads, ad_id)
        check_owner(self.request, int(ad.user_id))

        await delete_item(self.request["session"], ad)
        py_logger.info(f"/ads/{ad_id}")
        
        return raise_http_succeed(web.HTTPNoContent, message=None)