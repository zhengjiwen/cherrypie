from datetime import datetime
from .base import BaseModel


class User(BaseModel):
    __collection_name__ = 'user'

    fields = {
        'phone': str,
        'name': str,
        'sex': int,
        'state': int,
        "note": str,
        'created_at': datetime.utcnow,
        'passwd': str,
    }

    require_fields = {
        'phone': str,
        'name': str,
        'sex': int,
        'state': int,
        'passwd': str,
    }

    default_fields = {
        "created_at": datetime.utcnow
    }

    def get_user(self, user_id):
        return self.find_one({"_id": user_id})
