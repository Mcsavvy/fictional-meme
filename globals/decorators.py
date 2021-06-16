from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from . import render, error
from .utils import Attr
from .models import User
from .random_fields import Random
from .caching import CachedObject, dbcache
from api.templatetags.api import arg_parser


def test():
    print("works")


class Request:

    @staticmethod
    def on(
        request_event,
        handler_function,
    ):
        def bind(method):
            def function(self, request, *args, **kwargs):
                if request.headers.get('x-events') and\
                    request_event in arg_parser(
                        request.headers.get('x-events')
                )[1]:
                    return handler_function(self, request, *args, **kwargs)
                else:
                    if request_event.lower() in [
                        'post', 'get'
                    ]:
                        if bool(getattr(request, request_event.upper())):
                            return handler_function(request, *args, **kwargs)
                    elif request_event.lower() == "x-ajax":
                        if request.isAjax:
                            return handler_function(request, *args, **kwargs)
                    return method(self, request, *args, **kwargs)
            return function
        return bind

    @staticmethod
    def fake(
        **options
    ):
        _ = dict(
            path="/",
            user=Random.random(User),
            isAjax=Random.BooleanField(),
            headers={"X-Events": "??event=trigger"}
        )

        options = _ | options

        instance = HttpRequest()
        for k, v in options.items():
            setattr(instance, k, v)
        return instance

    @staticmethod
    def bind(request_event, handler_function):
        cached_obj = CachedObject(
            "request_handlers",
            cache=dbcache,
            version=1,
            timeout=None
        )
        handlers = set(cached_obj.get([]))
        handlers.add((
            request_event,
            handler_function
        ))
        cached_obj.set(list(handlers), timeout=None)
        return cached_obj

    @staticmethod
    def bind_method(allowed_methods=("POST", "GET")):
        def binder(view_func):
            def wrapper_func(self, request, *args, **kwargs):
                context = dict(
                    name="404",
                    reason=f"{request.method} Requests Not Allowed"
                )
                if isinstance(allowed_methods, str):
                    if request.method != allowed_methods:
                        return error(request, context)
                else:
                    if request.method not in allowed_methods:
                        return error(request, context)
                return view_func(self, request, *args, **kwargs)
            return wrapper_func
        return binder

    @staticmethod
    def ajax(ajax=None, view_func=None):
        """
        set ajax to True if this view only accepts ajax requests
        if a non-ajax request is sent:
            an error is thrown if view_func is None
            else the view_func is called with all arguments
        set ajax to false if this view doesn't accepts ajax request
        if an ajax request is sent:
            an error is thrown if view_func is None
            else the view_func is called with all arguments
        """
        def default_error(request, reason=""):
            context = dict(
                name="404",
                reason=reason or "Ajax Not Allowed Here."
            )
            return error(request, context)

        def binder(view):
            def wrapper_func(self, request, *args, **kwargs):
                if request.isAjax:
                    if ajax is True:
                        return view(
                            self,
                            request,
                            *args,
                            **kwargs
                        )
                    else:
                        if view_func:
                            return view_func(
                                self,
                                request,
                                *args,
                                **kwargs
                            )
                        else:
                            return default_error(
                                request
                            )
                else:
                    if ajax is False:
                        return view(
                            self,
                            request,
                            *args,
                            **kwargs
                        )
                    else:
                        if view_func:
                            return view_func(
                                self,
                                request,
                                *args,
                                **kwargs
                            )
                        else:
                            return default_error(
                                request,
                                "Only Ajax Request Allowed Here."
                            )
            return wrapper_func
        return binder
