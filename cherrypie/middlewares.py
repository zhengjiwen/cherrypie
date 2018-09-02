# -*- coding:utf-8 -*-

from bson import ObjectId
import json
import arrow
import falcon
from cherrypie.globals_obj import logging as logger
from cherrypie import errors
from cherrypie.globals_obj import db
import settings

_MAX_TTL_DELTA = 300


def timestamp(is_float=False):
    if is_float:
        return arrow.utcnow().float_timestamp
    else:
        return arrow.utcnow().timestamp


class AppTokenAuth(object):
    def process_resource(self, req, resp, resource, params):
        if not resource.require_authorize:
            return

    def process_response(self, req, resp, resource):
        pass


class Context(object):
    def process_request(self, req, resp):
        if req.method.lower() == 'options':
            _headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Methods': 'GET, POST, PUT',
                'Access-Control-Allow-Headers': ('X-AUTH, X-MSG-ID, X-APP-KEY, X-TOKEN, DNT,'
                                                 'X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,'
                                                 'If-Modified-Since,Cache-Control,Content-Type'),
                'Access-Control-Max-Age': '1728000',
            }
            raise falcon.HTTPError(falcon.HTTP_204, '', '', headers=_headers)

            # def process_request(self, req, resp):
            #     logging.warrninging(req)

    def process_response(self, req, resp, resource):
        resp.set_headers({
            'Access-Control-Allow-Origin': '*'
        })


class JSONTranslator(object):
    # NOTE: Starting with Falcon 1.3, you can simply
    # use req.media and resp.media for this instead.

    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
        #
        # See also: PEP 3333
        if req.content_length in (None, 0):
            # Nothing to do
            return

        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            req.context['doc'] = json.loads(body.decode('utf-8'))

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

    def process_response(self, req, resp, resource):
        if 'result' not in resp.context:
            return

        resp.body = json.dumps(resp.context['result'])
