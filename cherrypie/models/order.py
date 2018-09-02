from cherrypie import constants
from datetime import datetime
from bson import ObjectId
from .base import BaseModel


class Order(BaseModel):
    __collection_name__ = 'order'

    fields = {
        'state': int,
        "note": str,
        'resource_id': ObjectId,
        'operator_id': ObjectId,
        'created_at': datetime.utcnow,
        "time_quantum": list,
        "type": int,
        "code": str,
        "cancel_type": int,
    }

    require_fields = {
        'state': int,
        'date': int,
        'resource_id': ObjectId,
        'operator_id': ObjectId,
        "time_quantum": list,
    }

    default_fields = {
        "created_at": datetime.utcnow,
        "type": constants.ORDER_TYPE_PRACTICE
    }

    def check_schedule(self, date, resource_id):
        time_list = []
        for i in self.find({"date": date, "resource_id": resource_id, "state": constants.ORDER_STANDBY}):
            time_list.extend(i.get("time_quantum"))
        return time_list

    def create_order(self, docs):
        _id = self.create(docs)
        return self.update_set({'_id': _id}, {"code": str(_id)[-12:]})

    def find_list(self, spec, option):
        ret = self.find_objects(spec, option)

        resource_ids = [i.get("resource_id") for i in ret.get("results")]

        resource_dict = self.db.Resource.get_dict_with_id({"_id": {"$in": resource_ids}})

        for i in ret.get("results"):
            i.update({
                "resource_name": resource_dict.get(i.get("resource_id"), {}).get("name")
            })

        return ret
