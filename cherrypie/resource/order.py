from datetime import datetime
from bson import ObjectId
from .api_base import BaseResource
from cherrypie.utils import datetime_utils
from cherrypie import helper
from cherrypie import errors
from cherrypie.globals_obj import db
from cherrypie.globals_obj import logging
from cherrypie import constants


class Order(BaseResource):
    def on_get(self, req, resp):
        """Handles GET requests"""
        params = req.params
        account = req.context['account']
        state = int(params.get("state"))

        spec = {
            "operator_id": account.get("_id"),
            'state': state
        }

        option = {
            'page': 1,
            'limit': 30,
            "sort": [('created_at', -1)]

        }

        result = db.Order.find_list(spec, option)

        result['results'] = [helper.convert_result(i) for i in result.get("results")]

        resp.context['result'] = result

    @staticmethod
    def check_time(first_time):

        time_stamp = datetime_utils.get_work_time(datetime_utils.utc_today_int()).timestamp()
        if ((1800 * (first_time - 1)) + time_stamp) > datetime.utcnow().timestamp():
            return False
        return True

    def on_post(self, req, resp):
        params = req.context['doc']
        account = req.context['account']
        state = int(params.get("state", constants.ORDER_STANDBY))
        note = params.get('note', '')
        date = int(params.get('date'))
        resource_id = ObjectId(params.get("resource_id"))
        time_quantum = list(map(int, params.get("time_quantum")))

        self.check_time(time_quantum[0])

        if db.Order.find_one({"state": constants.ORDER_STANDBY, "type": constants.ORDER_TYPE_PRACTICE}):
            raise errors.ErrorOrderIsMax

        if db.Order.find({"date": {"$in": datetime_utils.get_month_list()}, "state": constants.ORDER_CANCELED,
                          "operator_id": account.get("_id")}).count() > 2:
            raise errors.ErrorOrderCancel

        if set(db.Order.check_schedule(date, resource_id)) & set(time_quantum):
            raise errors.ErrorOrderIsExists

        docs = {
            'state': state,
            'date': date,
            'resource_id': resource_id,
            'operator_id': account.get("_id"),
            "time_quantum": time_quantum,
            "note": note
        }

        _id = db.Order.create_order(docs)

        result = {
            "ok": True,
            "_id": str(_id)
        }
        resp.context['result'] = result


class OrderExtend(BaseResource):
    def on_get(self, req, resp, _id):
        """Handles GET requests"""
        # params = req.params

        rn = db.Order.get_from_oid(ObjectId(_id))

        result = helper.convert_result(rn)

        result.update({
            "resource_name": db.Resource.get_from_oid(ObjectId(result.get("resource_id"))).get("name")
        })

        resp.context['result'] = result

    def on_post(self, req, resp, _id):
        params = req.context['doc']
        state = int(params.get("state"))
        account = req.context['account']

        rn = db.Order.get_from_oid(ObjectId(_id))

        if not rn:
            raise errors.ErrorOrderNotFound

        if state == constants.ORDER_CANCELED and rn.get("state") == constants.ORDER_STANDBY:
            if db.Order.find({"date": {"$in": datetime_utils.get_month_list()}, "state": constants.ORDER_CANCELED,
                              "operator_id": account.get("_id")}).count() > 2:
                raise errors.ErrorOrderCancel
            db.Order.update_set({"_id": ObjectId(_id)},
                                {"state": constants.ORDER_CANCELED, "cancel_type": constants.ORDER_CANCEL_USER})

        result = {
            "ok": True,
            "_id": str(_id)
        }
        resp.context['result'] = result
