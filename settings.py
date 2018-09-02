# MONGODB
DB_NAME = 'cherrypie'
DB_HOST = '127.0.0.1'
DB_COLLECTIONS = [
    # 'cherrypie.models.code.Code',
    'cherrypie.models.token.Token',
    'cherrypie.models.user.User',
    'cherrypie.models.resource.Resource',
    'cherrypie.models.order.Order',
    # 'cherrypie.models.resource.Order',
]

# REDIS
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

RESOURCE = [
    {
        "name": 'cherrypie.resource.schedule.Schedule',
        "route": '/schedule',
    },
    {
        "name": 'cherrypie.resource.account.Account',
        "route": '/account',
    },
    # {
    #     "name": 'cherrypie.resource.auth.Auth',
    #     "route": '/auth',
    # },
    {
        "name": 'cherrypie.resource.auth.Login',
        "route": '/login',
    },
    {
        "name": 'cherrypie.resource.auth.LoginOut',
        "route": '/loginout',
    },
    {
        "name": 'cherrypie.resource.order.Order',
        "route": '/order',
    },
    {
        "name": 'cherrypie.resource.order.OrderExtend',
        "route": '/order/{_id}',
    },
    {
        "name": 'cherrypie.resource.resource.Resource',
        "route": '/resource',
    },
]

MIDDLEWARES = [
    'cherrypie.middlewares.JSONTranslator',
    'cherrypie.middlewares.Context',
    'cherrypie.middlewares.AppTokenAuth',
]

secret_key = "daklsfklasdfjqljajdfljlf"

DEBUG = True

TEST_AUTH_CODE = 666666
