from .api_base import BaseResource
from cherrypie import errors
from cherrypie.globals_obj import db
from cherrypie.globals_obj import logging


class Token(BaseResource):
    def on_get(self, req, resp):
        """Handles GET requests"""
        # params = req.params
        # print(params.get("phone"), params.get("code"))

        if True:
            raise errors.AccountNotFound
        result = {"ok": True}
        resp.context['result'] = result
