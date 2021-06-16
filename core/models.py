from django.db import models
from django.contrib.auth.models import User
import random
from string import ascii_letters
import os
import sys
from datetime import timedelta
from django.utils import timezone
import os


# Create your models here.


# User Profile Model
class AddressAndInfo(models.Model):
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    home_street = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    node = models.OneToOneField(
        to="Node", on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    info = models.OneToOneField(
        to=AddressAndInfo, on_delete=models.CASCADE, blank=True, null=True)
    node = models.OneToOneField(
        "Node", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.first_name.title()} {self.last_name.title()}"


class Theme(models.Model):
    name = models.CharField(max_length=20, default='default')
    lt = models.CharField(max_length=20, default='#FFFAF3')
    dk = models.CharField(max_length=20, default='#262626')
    pm = models.CharField(max_length=20, default='#FF503F')
    sc = models.CharField(max_length=20, default='#FF503F')
    dm = models.BooleanField(default=False)
    glass = 'transparent'
    shadow = "rgba(0, 0, 0, 0.7)"

    def toggle_colour(SELF, LIGHT_MODE, DARK_MODE):
        if SELF.dm:
            return getattr(SELF, (DARK_MODE), None)
        return getattr(SELF, (LIGHT_MODE), None)

    def get(self, colour, fallback=lambda *x: None):
        if not isinstance(colour, str):
            return
        if colour in "lt dk pm sc dm glass shadow":
            return getattr(self, (colour))
        if len(colour.split("-")) == 2:
            return self.toggle_colour(*colour.split("-"))
        if colour == "bg":
            return self.get("lt-dk")
        if colour == "gb":
            return self.get("dk-lt")
        if colour == "ab":
            return self.get("pm-sc")
        if colour == "ba":
            return self.get("sc-pm")
        return fallback(colour)

    def __str__(self):
        return self.name


class Node(models.Model):
    user = models.OneToOneField(User, models.CASCADE, related_query_name="node")
    theme = models.ForeignKey(
        Theme, on_delete=models.DO_NOTHING, null=True, blank=True,
        related_name="user"
    )

    def __str__(self):
        return self.user.username

    def isOnDarkMode(self):
        return self.theme.dm

    @property
    def get_notifications(self):
        return self.notifications.all()

    @property
    def get_orders(self):
        return self.order_set.all()

    @property
    def get_ordered_items(self):
        return self.orderitem_set.all()

    @property
    def get_profile(self):
        try:
            return self.profile
        except Exception as err:
            if "has no profile" not in str(err):
                raise

    @property
    def get_info(self):
        try:
            return self.addressandinfo
        except Exception as err:
            if "has no addressandinfo" not in str(err):
                raise

    @property
    def get_viewed_products(self):
        return self.viewed_products.all()

    @property
    def get_wishes(self):
        return self.wishlist_set.all()


class Notification(models.Model):
    owner = models.ForeignKey(
        Node,
        on_delete=models.CASCADE,
        related_name="notifications"
    )
    message = models.TextField()
    level = models.CharField(max_length=7, default="info")
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<{0}! notification for {1}>".format(self.level, self.owner)


class PopulationError(Exception):
    pass


