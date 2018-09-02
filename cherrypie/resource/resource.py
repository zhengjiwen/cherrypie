from .api_base import BaseResource
from cherrypie import helper
from cherrypie import errors
from cherrypie.globals_obj import db
from cherrypie.globals_obj import logging
from cherrypie import constants


class Resource(BaseResource):
    def on_get(self, req, resp):
        """Handles GET requests"""
        params = req.params

        spec = {
            'state': constants.ENABLED
        }

        option = {
            'page': 1,
            'limit': 30
        }

        result = db.Resource.find_objects(spec, option)

        result['result'] = [helper.convert_result(i) for i in result.get("results")]

        resp.context['result'] = result

    def on_post(self, req, resp):
        params = req.context['doc']
        account = req.context['account']
        name = str(params.get("name"))
        resource_type = int(params.get("type"))
        state = int(params.get("state"))
        note = params.get('note', '')

        docs = {
            'name': name,
            'state': state,
            'type': resource_type,
            'note': note
        }

        _id = db.Resource.create(docs)

        result = {
            "ok": True,
            "_id": str(_id)
        }
        resp.context['result'] = result
