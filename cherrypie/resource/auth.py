import hmac
from bson import ObjectId
from random import randint
from .api_base import BaseResource
from cherrypie import errors
from cherrypie.globals_obj import db
from cherrypie.utils.auth import hash_passwd
from cherrypie.globals_obj import logging
from cherrypie import constants
import settings


#
# class Auth(BaseResource):
#     def on_get(self, req, resp):
#         """Handles GET requests"""
#         params = req.params
#         phone = str(params.get("phone"))
#
#         if not db.User.find_one({"phone": phone, 'state': constants.ENABLED}):
#             raise errors.AccountNotFound
#
#         info = db.Code.find_one({"phone": phone})
#
#         if info:
#             code = info.get("code")
#         else:
#             code = randint(100001, 999999)
#             db.Code.create({
#                 "phone": phone,
#                 "code": code,
#             })
#
#         result = {
#             "ok": True,
#             "code": code,
#         }
#         resp.context['result'] = result
#
#     def on_post(self, req, resp):
#         pass


class Login(BaseResource):


    def on_get(self, req, resp):
        """Handles GET requests"""
        params = req.params
        try:
            phone = params.get("phone")
            passwd = params.get("passwd")
        except TypeError:
            raise errors.ErrorInvalidArgument

        user_info = db.User.find_one({"phone": phone})

        if not user_info:
            raise errors.AccountNotFound

        if hash_passwd(passwd.encode("utf-8")) != user_info.get("passwd"):
            raise errors.ErrorPassword

        token = str(db.Token.create_token(user_info.get("_id")))

        user_info.update({"_id": str(user_info.get("_id"))})
        user_info.update({"created_at": str(user_info.get("created_at"))})

        result = {
            "ok": True,
            'token': token,
            'user': user_info,
        }
        resp.context['result'] = result


class LoginOut(BaseResource):
    def on_post(self, req, resp):
        """Handles GET requests"""
        params = req.context['doc']
        access_token = params.get("access_token")

        token = db.Token.get_from_oid(ObjectId(access_token))

        if not token:
            raise errors.ErrorAccessTokenInvalid

        db.Token.revoke(token.get("_id"))

        result = {
            "ok": True,
        }
        resp.context['result'] = result
