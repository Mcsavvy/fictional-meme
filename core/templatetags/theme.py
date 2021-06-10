from django import template
from ..models import *

register = template.Library()
new = register.filter

try:
    default = Theme.objects.get(name="default")
except Theme.DoesNotExist:
    default = Theme.objects.create(name="default")


@new('get_theme')
def get(username, colour):
    if not username:
        return default.get(colour, lambda *x: "red")
    try:
        user = User.objects.get(username=username)
        node = Node.objects.get(user=user)
        if not node.theme:
            node.theme = Theme.objects.create(name=user.username)
            node.save()
        return node.theme.get(colour, fallback=lambda *x: "red")
    except Exception:
        return default.get(colour, lambda *x: "red")


@new("which_theme")
def which(username):
    try:
        user = User.objects.get(username=username)
        node = Node.objects.get(user=user)
        if not getattr(
            node.theme,
            'name',
            None
        ):
            node.theme = default
            node.save()
        return getattr(
            node.theme,
            'name',
        )
    except Node.DoesNotExist:
        return "NON-EXISTING-NODE"


@new("theme_toggle")
def toggle(user, filter=""):
    filters = filter.split("&&")
    dm = get(user.username, "dm")
    if isinstance(dm, bool) and dm:
        if len(filters) == 1:
            return filters[0]
        if len(filters) == 2:
            return filters[1]
        else:
            return filter
    elif isinstance(dm, bool) and not dm:
        if len(filters) == 1:
            return filters[0]
        if len(filters) == 2:
            return filters[0]
        else:
            return filter
    else:
        return filter
