from datetime import datetime
from .base import BaseModel


class Resource(BaseModel):
    __collection_name__ = 'resource'

    fields = {
        'name': str,
        'type': int,
        'state': int,
        "note": str,
        'created_at': datetime.utcnow,
    }

    require_fields = {
        'name': str,
        'type': int,
        'state': int,
    }

    default_fields = {
        "created_at": datetime.utcnow
    }

    def get_user(self, user_id):
        return self.find_one({"_id": user_id})
