from django.contrib import messages
from django.views.decorators.cache import cache_page
from globals.models import (
    Order,
    OrderItem, OrderItems,
    Product, Products,
    WishList, Wishlists,
    Node, Brand, Category,
    Coupon
)
from django.shortcuts import redirect
from core.decorators import allowed_user, bind_request
from django.contrib.auth.decorators import login_required
from globals import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page


# Create your views here.
@bind_request("GET")
def shop_page(request):
    all_products = Product.objects.all()
    if request.GET.get('ajax'):
        context = dict(
            products=all_products,
        )
        return render(request, 'shop/shop-page.html', context)

    filters = {
        "category": None,
        "max_price": None,
        "min_price": None,
        "featured_only": None,
        "top_only": None,
        "Brand": None,
    }
    for filter in filters:
        filters[filter] = request.GET.get(filter)
    if filters['max_price']:
        all_products = all_products.filter(
            price__lte=float(filters['max_price']),
            price__gte=float(filters['min_price']),
        )
    if filters['featured_only'] == "":
        all_products = all_products.filter(featured=True)
    if filters['top_only'] == "":
        all_products = all_products.filter(top_product=True)
    if filters['category']:
        all_products = all_products.filter(
            categories__name=str(filters['category'])
        )
    if filters['Brand']:
        all_products = all_products.filter(
            brand__name=str(filters['Brand'])
        )
    max_price = max(
        Products(
            query=all_products
        ).query.all_prices or Products().all_prices
    )
    min_price = min(
        Products(
            query=all_products
        ).query.all_prices or Products().all_prices
    )
    for i in [
        "category", "max_price", "min_price",
        "featured_only", "top_only"
    ]:
        print(i + ": ", request.GET.get(i))
    context = dict(
        products=all_products,
        max_price=max_price,
        min_price=min_price
    )

    return render(request, 'shop/shop-page.html', context)


@login_required(login_url='auth')
def single_product_page(request, slug):
    node = Node.objects.get(user=request.user)
    product = Product.objects.get(slug=slug)
    product.viewers.add(node)
    product.save()
    products = []
    related_by_categories = set()
    for x in Product.objects.all():
        for y in x.categories.all():
            if y in product.categories.all() and x.name != product.name:
                related_by_categories.add(x)
    related_by_viewer = set()
    for p in node.viewed_products.all():
        if p.name != product.name:
            related_by_viewer.add(p)
    products += list(related_by_categories)
    products += list(related_by_viewer)
    context = {
        'product': product,
        'products': products[:13]
    }
    print(products)
    return render(request, 'shop/product-single.html', context)


@login_required(login_url='auth')
@allowed_user(allowed_roles=['customer'])
def cart_page(request):
    node = Node.objects.get(user=request.user)
    context = {
        "cart": node.get_ordered_items.filter(ordered=False),
        'total': 0.0,
        'orders': node.get_orders
    }
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        item_name = request.POST.get("item")
        target = context['cart'].get(name=item_name)
        target.quantity = quantity
        target.save()
    for item in context['cart']:
        context['total'] += item.price
    return render(request, 'shop/cart-page.html', context)


def add_to_cart(request, itemId):
    if not request.user.is_authenticated:
        data = {"message": "Unauthorized user.", "level": "error"}
        return JsonResponse(data)
    try:
        node = Node.objects.get(user=request.user)
        product = Product.objects.get(id=itemId)
        response = OrderItems() + OrderItem(
            name=product.name,
            owner=node,
            slug=product.slug,
            image=product.image.name,
            cost=product.discounted_price,
        )
        if response == "OK":
            data = {
                "message": "{0} has been added to your cart.".format(
                    product.name
                ),
                "level": "success"
            }
        elif response == "DUPLICATE":
            data = {
                "message": "{0} is already in your cart.".format(
                    product.name
                ),
                "level": "info"
            }
    except Node.DoesNotExist:
        data = {"message": "Unauthorized User.", "level": "error"}
    except Product.DoesNotExist:
        data = {"message": "Non Existing Product.", "level": "error"}
    return JsonResponse(data)


@login_required(login_url='auth')
@allowed_user(allowed_roles=['customer'])
def delete_cart_item(request, id):
    order = OrderItem.objects.get(id=id)
    name = str(order.name)
    order.delete()
    data = dict(
        message="{0} has been removed from your cart".format(
            name
        ),
        level="success"
    )
    return JsonResponse(data)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def checkout(request):
    node = Node.objects.get(user=request.user)
    items = OrderItem.objects.filter(
        owner=node, ordered=False)
    if not items:
        messages.warning(request, "Add items to cart first.")
        return redirect('cart')
    order = Order(
        owner=node,
    )
    order.save()
    for i in items:
        order.items.add(i)
    order.save()
    for i in items:
        i.ordered = True
        i.save()
    return redirect('cart')


def add_to_wish_list(request, itemId):
    if not request.user.is_authenticated:
        data = {"message": "Unauthorized user.", "level": "error"}
        return JsonResponse(data)
    try:
        node = Node.objects.get(user=request.user)
        product = Product.objects.get(id=itemId)
        response = Wishlists() + WishList(
            owner=node,
            item=product
        )
        if response == "OK":
            data = {
                "message": "{0} has been added to your wishlist.".format(
                    product.name
                ),
                "level": "info"
            }
        elif response == "DUPLICATE":
            WishList.objects.get(item=product).delete()
            data = {
                "message": "{0} has been removed from your wishlist.".format(
                    product.name
                ),
                "level": "info"
            }
    except Node.DoesNotExist:
        data = {"message": "Unauthorized user.", "level": "error"}
    except Product.DoesNotExist:
        data = {"message": "Non Existing Product.", "level": "error"}
    return JsonResponse(data)


@login_required(login_url='auth')
@allowed_user(allowed_roles=['customer'])
def delete_wish(request, id):
    product = Product.objects.get(id=id)
    WishList.objects.get(item=product).delete()
    messages.success(
        request,
        "{0} has been removed from your wishlist".format(
            product.name
        )
    )
    return redirect('wishlist')


@login_required(login_url='auth')
@allowed_user(allowed_roles=['customer'])
def clear_wish(request):
    node = Node.objects.get(user=request.user)
    wishlist = WishList.objects.filter(owner=node)
    if not wishlist:
        messages.warning(request, "Nothing to clear.")
    for item in wishlist:
        item.delete()
    return redirect('wishlist')


@login_required(login_url='auth')
@allowed_user(allowed_roles=['customer'])
def wishlist_page(request):
    node = Node.objects.get(user=request.user)
    context = {
        'wishlist': WishList.objects.filter(owner=node)
    }
    return render(request, 'shop/wish-page.html', context)


@login_required(login_url='auth')
@allowed_user(allowed_roles=['customer'])
def create_cart_from_wishlist(request):
    node = Node.objects.get(user=request.user)
    wishlist = WishList.objects.filter(owner=node)
    if not wishlist:
        messages.warning(request, "Add items to wishlist first.")
        return redirect('wishlist')
    for item in wishlist:
        node = Node.objects.get(user=request.user)
        OrderItems() + OrderItem(
            name=item.item.name,
            owner=node,
            slug=item.item.slug,
            image=item.item.image.name,
            cost=item.item.discounted_price,
        )
        item.delete()
    return redirect('cart')


@login_required(login_url='auth')
@allowed_user(allowed_roles=['customer'])
@bind_request("POST")
def apply_coupon_to_order(request):
    code = request.POST.get("code")
    order_id = request.POST.get("order_id")
    print(request.POST)
    print(code, order_id)
    if not code:
        data = dict(
            message="No Coupon Found",
            level="error"
        )
    elif not order_id:
        data = dict(
            message="Order Not Specified",
            level="error"
        )
    try:
        order = Order.objects.get(id=order_id)
        status = order.apply_coupon(code)
        if status != "OK":
            data = {
                "message": status,
                "level": "warning"
            }
        else:
            data = {
                "message": "{0} applied!".format(code),
                "level": "success"
            }
    except Order.DoesNotExist:
        data = dict(
            message="Order  Not Specified",
            level="error"
        )
    return JsonResponse(data)
