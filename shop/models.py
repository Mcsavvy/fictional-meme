from core.models import (
    Node
)
from globals.random_fields import Random
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import uuid
from django.utils import timezone
# Create your models here.


def wrapper(function, *args, **kwargs):
    def inner():
        return function(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default="")
    slug = models.SlugField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def url(self):
        return reverse("shop") + "?Brand={0}".format(
            self.name
        )


class Banner(models.Model):
    image = models.ImageField(null=True, blank=True)
    message = models.TextField(blank=True, default="")
    creation_date = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(
        default=wrapper(Random.DateTimeField, "days", blank=True)
    )
    link = models.URLField(null=True, blank=True)
    link_text = models.CharField(max_length=50, default="Get Started")

    @property
    def expired(self):
        return (self.expiry_date <= timezone.now())

    def __str__(self):
        return "<Slide {0}>".format(self.id)


class Category(models.Model):
    name = models.CharField(max_length=45)
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_query_name="children",
        on_delete=models.CASCADE
    )
    description = models.TextField(
        blank=True,
        default="This may come as a surprise to you but..."
    )
    slug = models.SlugField()
    image = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def url(self):
        return reverse("shop") + "?category={0}".format(
            self.name
        )

    class Meta:
        verbose_name_plural = "categories"


class Coupon(models.Model):
    code = models.CharField(
        max_length=25,
        default=wrapper(Random.Charfield, max_length=10, prefix="COUPON")
    )
    discount = models.FloatField(default=0.0)
    applied = models.BooleanField(default=False)
    usage = models.IntegerField(default=0)
    orders = models.ManyToManyField(to="Order", blank=True)
    created = models.DateTimeField(auto_now=True)
    expire = models.DateTimeField(
        default=wrapper(Random.DateTimeField, "days")
    )

    def __str__(self):
        return self.code

    def apply(self, order):
        discounted_price = (float(self.discount) / 100.0) * float(order.price)
        order.total_price -= discounted_price
        order.save()
        self.applied = True
        self.usage += 1
        self.orders.add(order)
        self.save()
        return "OK"

    @property
    def users(self):
        _ = []
        for order in self.orders.all():
            _.append(order.owner)
        return _


class OrderItem(models.Model):
    name = models.CharField(
        max_length=45,
        default=wrapper(Random.Charfield(45, "Order "))
    )
    cost = models.FloatField(default=10.0)
    slug = models.SlugField()
    image = models.ImageField(null=True)
    owner = models.ForeignKey(Node, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def price(self):
        return self.cost * self.quantity

    class Meta:
        verbose_name = "Ordered Item"
        verbose_name_plural = "Ordered Items"


class Order(models.Model):
    ref_code = models.UUIDField(default=uuid.uuid4)
    owner = models.ForeignKey(Node, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    total_price = models.FloatField(default=0.0)
    calculated = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.ref_code)

    @property
    def price(self):
        if not self.calculated:
            cost = float(0)
            for order in self.items.all():
                cost += float(order.price)
            self.total_price = float(cost)
            self.calculated = True
            self.save()
        return float(self.total_price)

    @price.setter
    def price(self, new_price):
        if not new_price <= 0.0:
            self.total_price = new_price
            self.calculated = True
            self.save()
        return self.price

    @price.deleter
    def price(self):
        self.total_price = 0.0
        self.save()

    def apply_coupon(self, code):
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return "Coupon Does Not Exist"
        if self in coupon.orders.all():
            return "Coupon Already Applied"
        if self.price <= 0.0:
            return "Minimum Order Price Reached"
        return coupon.apply(self)

    @property
    def get_coupons(self):
        return self.coupon_set.all()

    @property
    def items_count(self):
        return len(self.items.all())


class Product(models.Model):
    name = models.CharField(max_length=45)
    price = models.FloatField(default=10.0)
    slug = models.SlugField()
    image = models.ImageField()
    featured = models.BooleanField(default=False)
    top_product = models.BooleanField(default=False)
    categories = models.ManyToManyField(
        to=Category,
        blank=True,
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_query_name="products",
        null=True
    )
    discount = models.FloatField(default=0.0)
    viewers = models.ManyToManyField(
        to=Node,
        blank=True,
        related_name="viewed_products"
    )

    @property
    def url(self):
        kwargs = {
            'slug': self.slug
        }
        return reverse('product.single', kwargs=kwargs)

    @property
    def discounted_price(self):
        return float(self.price) - self.discounted

    @property
    def discounted(self):
        return (float(self.discount) / 100.0) * float(self.price)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug)
        super(Product, self).save(*args, **kwargs)

    def add_viewer(self, user):
        try:
            node = Node.objects.get(user=user)
        except Node.DoesNotExist:
            return
        if node not in self.viewers.all():
            self.viewers.add(node)

    def add_discount(self, discount):
        discount = float(discount)
        self.discount += discount
        self.save()

    def __str__(self):
        return self.name


class WishList(models.Model):
    owner = models.ForeignKey(Node, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.owner)
