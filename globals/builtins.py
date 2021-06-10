from .template import builtins
from .models import *
import re
from core.templatetags.theme import get
import random

@builtins.register("colour_list", timeout=0, resolve_dict=False)
def foo(request):
    colour_list = {}
    for i in [
        'dk', 'lt', 'pm', 'sc',
        'bg', 'gb', 'ab', 'ba',
        "dk-pm", "dk-sc",
        "lt-pm", "lt-sc",
        "pm-dk", "pm-lt",
        "sc-dk", "sc-lt",
        "glass", "shadow",
        "shadow-glass",
        "glass-shadow",
    ]:
        colour_list[i] = get(request.user.username, i)
    return colour_list


builtins.register(
    "site_info",
    timeout=None
)(
    {
        "site_name": "Soar-Tech",
        "currency": "$",
        "font_sizes": list(range(33)),
        "border_radius": [
            "top-left", "bottom-left",
            "top-right", "bottom-right"
        ],
    }
)


@builtins.register("banners", timeout=None)
def show_banner(request):
    accepted_urls = [r"^/?$", r"shop/?$"]
    for url in accepted_urls:
        if re.search(url, request.path) and not builtins.request.get("error"):
            return Banner.objects.all()


@builtins.register("filters", timeout=60 * 60)
def filters(request):
    return {
        "categories": sorted(Categories().all_names),
        "brands": sorted(Brands().all_names)
    }


@builtins.register("notification", timeout=None)
def notifications(request):
    default = {
        "has_notification": False,
        "notifications": []
    }
    if not request.user.is_authenticated:
        return default
    try:
        node = Node.objects.get(user=request.user)
    except Node.DoesNotExist:
        return default
    notifications = node.get_notifications
    default['has_notification'] = bool(notifications)
    default['notifications'] = notifications
    return default


@builtins.register("user_agent", timeout=60 * 60)
def user_agent(request):
    from django_user_agents.utils import get_user_agent
    user_agent = get_user_agent(request)
    default = {
        "is_mobile": None,
        "is_tablet": None,
        "is_touch_capable": None,
        "is_pc": None,
        "is_bot": None
    }
    for obj in default:
        try:
            default[obj] = getattr(user_agent, obj)
        except Exception:
            continue
    return default


@builtins.register("available_coupons", timeout=60 * 60)
def get_unused_coupons(request):
    default = []
    if not request.user.is_authenticated:
        return default
    node = Node.objects.get(user=request.user)
    for coupon in Coupon.objects.all():
        if node not in coupon.users:
            default.append(coupon)
    random.shuffle(default)
    return default[:2]
