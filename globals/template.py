from django.shortcuts import render
import sys
import traceback
from .caching import CachedObject, dbcache


CachedObject.settings['cache'] = dbcache


class Builtin:
    settings = dict(
        cache=True,
        timeout=0,
        resolve_dict=True,
        resolve_function=True,
        ajax=None,
    )

    def __init__(self, **kwargs):
        self.VARS = []
        self.request = {}
        self.request.update(kwargs)

    def register(self, name="var", **settings):
        def register(obj):
            self.VARS.append((name, obj, settings))
            return obj
        return register

    def __call__(self, request):
        vars = {}
        for name, var, settings in self.VARS:
            settings = self.settings | settings
            if request.isAjax:
                if settings['ajax'] is False:
                    continue
            else:
                if settings['ajax'] is True:
                    continue
            if callable(var):
                if not settings.get('resolve_function'):
                    vars[name] = CachedObject(name).get(
                        default=var,
                        timeout=settings.get('timeout')
                    )
                    continue
                result = var(request)
                if isinstance(result, dict) and settings.get('resolve_dict'):
                    for k in result:
                        if settings.get('cache'):
                            vars[k] = CachedObject(k).get(
                                result[k],
                                timeout=settings.get("timeout")
                            )
                    continue
                vars[name] = CachedObject(name).get(
                    result,
                    timeout=settings.get('timeout')
                )
                continue
            if isinstance(var, dict) and settings.get('resolve_dict'):
                for k in var:
                    if settings.get('cache'):
                        vars[k] = CachedObject(k).get(
                            var[k],
                            timeout=settings.get("timeout")
                        )
                continue
            else:
                vars[name] = CachedObject(name).get(
                    var,
                    timeout=settings.get("timeout")
                )
        return vars


builtins = Builtin()


def render_error(request, context):
    from .builtins import builtins as BUILTINS
    context.update(BUILTINS(request))
    return render(request, 'error.html', context)


def error(request, err=None, **extra):
    """Only use this in an exception"""
    from .builtins import builtins as BUILTINS
    BUILTINS.request['error'] = True
    context = dict(
        name="404",
        thrown=str(err[0]).strip('<class').rstrip('>'),
        reason=err[1],
        tracebacks=traceback.format_tb(err[2])
    )
    context.update(BUILTINS(request))
    context.update(extra)
    return render_error(request, context)


def render_template(request, page, context={}, debug=False):
    from .builtins import builtins as BUILTINS
    if debug or ("no-err" in request.GET):
        context.update(BUILTINS(request))
        return render(request, page, context)
    try:
        context.update(BUILTINS(request))
        data = render(request, builtins.request.get('template', page), context)
        return data
    except Exception:
        BUILTINS.request['error'] = True
        return error(request, sys.exc_info())