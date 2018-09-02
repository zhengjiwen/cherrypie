from datetime import datetime
from cherrypie.utils import datetime_utils
from bson import ObjectId
from .api_base import BaseResource
from cherrypie import helper
from cherrypie import errors
from cherrypie.globals_obj import db
from cherrypie.globals_obj import logging
from cherrypie import constants


class Schedule(BaseResource):
    @staticmethod
    def make_schedule(time_list, date):

        now_time = 1

        if date == datetime_utils.utc_today_int():
            if datetime.now().timestamp() < datetime_utils.get_work_time(datetime_utils.utc_today_int()).timestamp():
                now_time = 1
            else:
                ret = divmod((datetime.now().timestamp() - datetime_utils.get_work_time(
                    datetime_utils.utc_today_int()).timestamp()), 1800)
                if ret[1] > 0 and ret[0] == 0:
                    now_time = 2
                else:
                    now_time = ret[0]

        data_list = []
        for i in constants.TIME_QUANTUM:
            if i in time_list:
                state = constants.DISABLED
            else:
                state = constants.ENABLED

            if now_time > i:
                state = constants.DISABLED

            data_list.append({
                "time_quantum": i,
                "state": state,
            })
        return data_list

    def on_get(self, req, resp):
        """
        
        :param req: 
        :param resp: 
        :return: 
        """
        params = req.params

        resource_id = ObjectId(params.get("resource_id"))
        date = int(params.get("date"))

        result = self.make_schedule(db.Order.check_schedule(date, resource_id), date)

        resp.context['result'] = result

    def on_post(self, req, resp):
        """
        
        :param req: 
        :param resp: 
        :return: 
        """
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


class ScheduleExtend(BaseResource):
    def on_get(self, req, resp):
        """

        :param req: 
        :param resp: 
        :return: 
        """
        params = req.params
        account = req.context['account']
        resource_id = ObjectId(params.get("resource_id"))
        date = int(params.get("date"))

        result = self.make_schedule(db.Order.check_schedule(date, resource_id))

        resp.context['result'] = result
