# -*- coding: utf-8 -*-
#
# © 2010, 2011 SimpleGeo, Inc. All rights reserved.
# Author: Ian Eure <ian@simplegeo.com>
#

import sys
import logging
import json
from traceback import extract_stack

import decoroute
from webob import Request, Response, exc


logger = logging.getLogger('kestrelweb')


class JSONResponse(Response):

    """A response in JSON format."""

    default_content_type = 'application/json'

    def __init__(self, callback=None, **kwargs):
        body = self.serialize(kwargs.pop('body'))
        if callback is not None:
            self.default_content_type = 'application/javascript'
            body = '%s(%s);' % (callback, body)
        Response.__init__(self, body=body, charset='utf8', **kwargs)

    def serialize(self, obj):
        """Return this object as a JSON string."""
        return json.dumps(obj)


class App(decoroute.App):

    """API Core dispatcher."""

    def __init__(self, prefix='', key='dream.app'):
        decoroute.App.__init__(self, prefix, key)
        self.map = dict(((method, decoroute.UrlMap()) for method in ('HEAD', 'GET', 'POST', 'PUT', 'DELETE')))
        self.not_found(lambda e: exc.HTTPNotFound(detail='Not found'))
        self._render = self._render_response

    def route(self, env):
        """Route a request.

        Checks the method-specific map first, then the global as a fallback.
        """
        env[self._key] = self
        path, num = self._prefix[1].subn('', env['PATH_INFO'])
        if num != 1:
            raise exc.HTTPNotFound()

        try:
            endpoint, kwargs = self.map[env['REQUEST_METHOD']].route(path)
            return endpoint(Request(env, charset='utf-8'), **kwargs)

        except decoroute.NotFound, nfex:
            new_ex = exc.HTTPNotFound(' '.join(nfex.args))
            if not hasattr(new_ex, '__traceback__'):
                new_ex.__traceback__ = sys.exc_info()[-1]
            return new_ex

        except Exception, ex:
            logger.exception(ex)
            if not hasattr(ex, '__traceback__'):
                ex.__traceback__ = sys.exc_info()[-1]
            return ex

    def expose(self, pattern, method='GET', function=None, **kwargs):
        """Register a URL pattern for a specific HTTP method."""
        if method not in self.map:
            raise Exception('No such method: %s' % method)

        def decorate(function):
            """Add this function to the method map."""
            self.map[method].add(pattern, function, **kwargs)
            return function

        return decorate(function) if function else decorate

    def _mangle_response(self, resp):
        """Mangle the response, if warranted."""
        if (isinstance(resp, Response) and not isinstance(resp, exc.HTTPInternalServerError)):
            return resp

        if not isinstance(resp, Exception):
            resp = Exception('Expected a Response object, got %s instead.' % str(type(resp)))
            resp.__traceback__ = extract_stack()

        return _exception_to_response(resp)

    def _render_response(self, env, in_resp):
        """Render the Response object into WSGI format."""
        resp = self._mangle_response(in_resp)
        return (resp.status, resp.headers.items(), resp.app_iter)


def _exception_to_response(exception):
    """Return a JSONResponse representing an uncaught Exception."""
    return JSONResponse(status=getattr(exception, 'status', 500), body={
        'detail': (exception.detail or exception.explanation) if isinstance(exception, exc.HTTPException) else 'An internal error occured.',
    })
