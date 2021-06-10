from django import template
from ..models import *
import re
from api.templatetags.api import arg_parser

register = template.Library()
new = register.filter


@new()
def inwishlist(item_id, user):
    if not user.is_authenticated:
        return False
    try:
        node = Node.objects.get(user=user)
    except node.DoesNotExist:
        return False
    for item in node.get_wishes:
        if int(item_id) == item.item.id:
            return True
    return False


@new()
def incart(item_name, user):
    if not user.is_authenticated:
        return False
    try:
        node = Node.objects.get(user=user)
    except node.DoesNotExist:
        return False
    for item in node.get_ordered_items:
        if item_name == item.name:
            return True
    return False


@new()
def apply(function, arguments):
    args, kwargs = arg_parser(arguments)
    return function.__call__(*args, **kwargs)