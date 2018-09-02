from datetime import datetime, date, timedelta
from .base import BaseModel
from bson import ObjectId
from cherrypie import constants


def next_time(from_now=None, **kwargs):
    if from_now is None:
        from_now = datetime.utcnow()
    _next_time = from_now + timedelta(**kwargs)
    return _next_time


class Token(BaseModel):
    __collection_name__ = 'token'
    require_fields = {
        'account_id': ObjectId,
        "expired_at": datetime,
    }

    default_fields = {
        "state": constants.ENABLED,
        "created_at": datetime.utcnow
    }

    def create_token(self, account_id, ttl=30):
        expired_time = next_time(days=ttl)
        docs = {
            "account_id": account_id,
            'expired_at': expired_time
        }
        return self.create(docs)

    @staticmethod
    def is_ok(info):
        now = datetime.utcnow()
        return now < info['expired_at'] and info['state'] == constants.ENABLED

    def validate_access_token(self, access_token):
        token_info = self.find_one({"_id": ObjectId(access_token), "state": constants.ENABLED})
        if not token_info:
            return
        else:
            return token_info.get("account_id")

    def revoke(self, access_token):
        """作废request token"""

        doc = {
            'state': constants.DISABLED,
        }
        return self.update_set({"_id": access_token}, doc)
