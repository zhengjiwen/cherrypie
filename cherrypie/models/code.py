from datetime import datetime
from .base import BaseModel


class Code(BaseModel):
    __collection_name__ = 'code'

    require_fields = {
        'phone': str,
        'code': int,
    }

    default_fields = {
        "created_at": datetime.utcnow
    }
