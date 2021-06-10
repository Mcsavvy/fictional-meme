from shop.models import OrderItem, WishList
from core.models import Node


def get_cart_and_wish_count(request):
    if request.user.is_authenticated:
        try:
            node = Node.objects.get(user=request.user)
        except Node.DoesNotExist:
            return {
                'cart_count': 0,
                'wish_count': 0
            }
        cart = OrderItem.objects.filter(
            owner=node, ordered=False).count()
        wish = WishList.objects.filter(owner=node).count()
        return {
            'cart_count': cart,
            'wish_count': wish
        }

    else:
        return {
            'cart_count': 0,
            'wish_count': 0
        }


def get_cart_price(request):
    default = {"cart_price": 0.0}
    if not request.user.is_authenticated:
        return default
    try:
        node = Node.objects.get(user=request.user)
    except Node.DoesNotExist:
        return default
    for item in OrderItem.objects.filter(owner=node, ordered=False):
        default['cart_price'] += item.price
    return default
