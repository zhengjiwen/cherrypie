from cherrypie.globals_obj import db
from cherrypie.globals_obj import logging as logger
from .api_base import BaseResource
from cherrypie import errors
from cherrypie.utils.auth import hash_passwd


class Account(BaseResource):
    require_authorize = False

    def on_get(self, req, resp):
        """Handles GET requests"""

        result = {"ok": True}

        resp.context['result'] = result

    def on_post(self, req, resp):
        params = req.context['doc']
        phone = params.get("phone")
        name = params.get("name")
        sex = int(params.get("sex"))
        state = int(params.get("state"))
        note = params.get("note")
        passwd = params.get("passwd")

        if db.User.find_one({"phone": phone}):
            raise errors.ErrorPhoneIsExists

        docs = {
            'passwd': hash_passwd(passwd.encode('utf-8')),
            'phone': phone,
            'name': name,
            'sex': sex,
            'state': state,
            "note": note,
        }

        _id = db.User.create(docs)

        result = {
            'ok': True,
            "_id": str(_id)
        }
        resp.context['result'] = result
