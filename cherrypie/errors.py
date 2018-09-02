import json
from falcon.status_codes import HTTP_400, HTTP_401
from falcon.errors import HTTPError


class CherryPieError(HTTPError):
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "Access-Control-Allow-Origin": "*",
    }
    http_error_code = HTTP_400
    title = None
    description = {
        "code": "502",
        "zh_msg": "",
        "msg": "",
    }

    def __init__(self, **kwargs):
        super(CherryPieError, self).__init__(self.http_error_code, title=self.title,
                                             description=self.description, headers=self.headers, **kwargs)


class ErrorInvalidArgument(CherryPieError):
    http_error_code = HTTP_400
    title = None
    description = {
        "code": 500,
        "zh_msg": "参数缺失或错误",
        "msg": "ErrorInvalidArgument",
    }


class ErrorArgumentType(CherryPieError):
    http_error_code = HTTP_400
    title = None
    description = {
        "code": 501,
        "zh_msg": "参数类型错误",
        "msg": "ErrorArgumentType",
    }


class AccountNotFound(CherryPieError):
    http_error_code = HTTP_400
    title = None
    description = {
        "code": 502,
        "zh_msg": "账户错误",
        "msg": "AccountNotFound",
    }


class ErrorAccessTokenInvalid(CherryPieError):
    http_error_code = HTTP_401
    title = None
    description = {
        "code": 503,
        "zh_msg": "无效token或token已过期",
        "msg": "ErrorAccessTokenInvalid",
    }


class ErrorPhoneIsExists(CherryPieError):
    http_error_code = HTTP_400
    title = None
    description = {
        "code": 504,
        "zh_msg": "手机号已存在",
        "msg": "ErrorPhoneIsExists",
    }


class ErrorAuthCode(CherryPieError):
    http_error_code = HTTP_400
    title = None
    description = {
        "code": 505,
        "zh_msg": "验证码错误",
        "msg": "ErrorAuthCode",
    }


class ErrorOrderIsExists(CherryPieError):
    http_error_code = HTTP_400
    title = None
    description = {
        "code": 506,
        "zh_msg": "该时间段以预约",
        "msg": "ErrorOrderIsExists",
    }


class ErrorOrderIsMax(CherryPieError):
    http_error_code = HTTP_400
    title = None
    description = {
        "code": 507,
        "zh_msg": "有待使用预约单，无法预约",
        "msg": "ErrorOrderIsMax",
    }


class ErrorPassword(CherryPieError):
    http_error_code = HTTP_400
    title = None
    description = {
        "code": 508,
        "zh_msg": "手机号或密码错误",
        "msg": "ErrorPassword",
    }


class ErrorOrderNotFound(CherryPieError):
    http_error_code = HTTP_400
    title = None
    description = {
        "code": 509,
        "zh_msg": "未找到预约单",
        "msg": "ErrorOrderNotFound",
    }


class ErrorOrderCancel(CherryPieError):
    http_error_code = HTTP_400
    title = None
    description = {
        "code": 510,
        "zh_msg": "爽约超最大限额，无法操作",
        "msg": "ErrorOrderCancel",
    }
