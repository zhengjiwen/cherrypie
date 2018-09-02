from falcon import API
from falcon import api_helpers as helpers
from .helper import get_function


class CherryPie(API):
    def bootstrap(self, config):
        self.config = config
        self.load_middlewares()
        self.register_resource()
        return self

    def register_resource(self):
        for resource in self.config.RESOURCE:
            self.add_route(resource.get("route"), get_function(resource.get("name"))[0]())

    def load_middlewares(self):
        middleware = [get_function(i)[0]() for i in self.config.MIDDLEWARES]
        self._middleware = helpers.prepare_middleware(middleware)


def get_app(config):
    return CherryPie().bootstrap(config)
