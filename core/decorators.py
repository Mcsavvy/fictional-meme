from core.models import AddressAndInfo, Profile, Node
from django.http import HttpResponse
from django.shortcuts import redirect
from globals import render, error


def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                for grp in request.user.groups.all():
                    if grp.name in allowed_roles:
                        return view_func(request, *args, **kwargs)
            context = {
                "suggested": [
                    "This page maybe be restricted to a particular group."
                ],
                "name": 403,
                "reason": "Access Denied",
                "info": f"Allowed-Groups ({':'.join(allowed_roles)})"
            }
            return error(request, context)
        return wrapper_func
    return decorator


def profile_exists(view_func):
    def wrapper_func(request, *args, **kwargs):
        node = Node.objects.get(user=request.user)
        if Profile.objects.filter(node=node):
            return render(request, 'core/unauthorized.html')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def address_exists(view_func):
    def wrapper_func(request, *args, **kwargs):
        node = Node.objects.get(user=request.user)
        if AddressAndInfo.objects.filter(node=node):
            return render(request, 'user/unauthorized.html')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def bind_request(allowed_methods=("POST", "GET")):
    def binder(view_func):
        def wrapper_func(request, *args, **kwargs):
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
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return binder


def ajax_requests(ajax=None, view_func=None):
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
        def wrapper_func(request, *args, **kwargs):
            if request.isAjax:
                if ajax is True:
                    return view(
                        request,
                        *args,
                        **kwargs
                    )
                else:
                    if view_func:
                        return view_func(
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
                        request,
                        *args,
                        **kwargs
                    )
                else:
                    if view_func:
                        return view_func(
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
