from datetime import datetime
from bson import ObjectId
import importlib
from cherrypie.utils import datetime_utils


def get_function(path):
    module_path, func_name = path.rsplit('.', maxsplit=1)
    return (getattr(importlib.import_module(module_path), func_name), func_name)


def convert_result(result):
    for k, v in result.items():
        if isinstance(v, ObjectId):
            result[k] = str(v)
        if isinstance(v, datetime):
            result[k] = str(datetime_utils.get_local_time(v))

    return result
