from django.contrib.auth.models import User
from shop.models import (
    Category, Banner, Product,
    OrderItem, Order, WishList,
    Brand, Coupon
)
from core.models import (
    AddressAndInfo, Profile,
    Theme, Node, Notification
)
from pages.models import Contact
from .utils import Attr


class Model:
    model = None
    searchable = []
    required = []
    Return = {
        "not_found": "DOESNOTEXIST",
        "duplicate": "DUPLICATE",
        "success": "OK",
        "failed": "FAIL"
    }

    def __init__(self, **queries):
        self.fields = [
            f.name for f in self.model._meta.local_fields
        ]
        if not self.searchable:
            self.searchable = [_ for _ in self.fields if _ != "id"]
        if not self.required:
            self.required = [_ for _ in self.fields if _ != "id"]
        self.all = self.model.objects.all()
        for field in self.fields:
            setattr(
                self,
                "all_{0}s".format(field),
                [getattr(instance, field) for instance in self.all]
            )
        for key, query in queries.items():
            this = Attr(query)
            setattr(self, key, this)
            for field in self.fields:
                setattr(
                    this,
                    "all_{0}s".format(field),
                    [getattr(instance, field) for instance in query]
                )

    def __iter__(self):
        return iter(self.all)

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.__dict__.get(attr)
        return getattr(self.model, attr)

    def __add__(self, instance):
        matches = []
        for model in self.all:
            match = []
            for field in self.searchable:
                match.append(
                    getattr(model, field) == getattr(instance, field)
                )
            matches.append(match)
        for match in matches:
            if all(match):
                return self.Return.get("duplicate")
        instance.save()
        self.__init__()
        return self.Return.get("success")

    def __sub__(self, instance):
        fields = {
            field: getattr(instance, field) for field in self.searchable
        }
        try:
            wanted = self.model.objects.get(**fields)
            wanted.delete()
            self.__init__()
            return self.Return.get("success")
        except self.model.DoesNotExist:
            return self.Return.get("not_found")

    def init(self, **fields):
        _ = {}
        if not fields:
            return self.Return["failed"]
        for field in self.required:
            if not fields.get(field):
                return "'%s' *REQUIRED*" % field
        for field in self.fields:
            try:
                _[field] = fields[field]
            except KeyError:
                pass
        new_instance = self.model(**_)
        Return = self + new_instance
        if Return != self.Return["success"]:
            return Return
        return new_instance


class Nodes(Model):
    model = Node
    searchable = ["user"]


class Themes(Model):
    model = Theme
    searchable = ["pm", "sc"]


class Wishlists(Model):
    model = WishList
    searchable = ["owner", "item"]


class Categories(Model):
    model = Category


class Brands(Model):
    model = Brand


class Coupons(Model):
    model = Coupon


class Products(Model):
    model = Product
    required = [
        "name", "price", "slug", "image",
        "category",
    ]


class OrderItems(Model):
    model = OrderItem
    searchable = ["owner", "name", "price"]
    required = searchable


class Orders(Model):
    model = Order
    searchable = [
        "ref_code", "owner", "items", "price"
    ]
    required = searchable


class Users(Model):
    model = User
    searchable = ["email", "username"]
    required = searchable


class Notifications(Model):
    model = Notification


def nodify(user):
    if not isinstance(user, User):
        raise Exception("User object needed.")
    username = user.username
    theme = Theme.objects.create(name=username)
    new_node = Node(user=user, theme=theme)
    return Nodes() + new_node