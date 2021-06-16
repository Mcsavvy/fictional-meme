from .template import builtins
from .models import *
import re
import random


@builtins.register("colour_list", timeout=None, ajax=False)
def colour_list(request):
    return [
        'bg', 'pm', 'sh', 'sc',
        'r-bg', 'r-pm', 'r-sh', 'r-sc',
        'lt-bg', 'lt-pm', 'lt-sh', 'lt-sc',
        'dk-bg', 'dk-pm', 'dk-sh', 'dk-sc'
    ]


builtins.register(
    "site_info",
    timeout=None,
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


@builtins.register(
    "banners",
    timeout=None,
    ajax=False
)
def show_banner(request):
    accepted_urls = [r"^/?$", r"shop/?$"]
    for url in accepted_urls:
        if re.search(url, request.path) and not builtins.request.get("error"):
            return Banner.objects.all()


@builtins.register(
    "filters",
    timeout=60 * 60,
    ajax=False
)
def filters(request):
    return {
        "categories": sorted(Categories().all_names),
        "brands": sorted(Brands().all_names)
    }


@builtins.register("counters")
def counters(request):
    default = {
        "notifications": 0,
        "cart_count": 0,
        "wish_count": 0,
    }
    if not request.user.is_authenticated:
        return default
    try:
        node = Node.objects.get(user=request.user)
    except Node.DoesNotExist:
        return default
    default['notifications'] = len(node.get_notifications)
    default['cart_count'] = len(node.get_ordered_items)
    default['wish_count'] = len(node.get_wishes)
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


@builtins.register(
    "available_coupons",
    timeout=60 * 60,
    ajax=False
)
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
