from .populate import (
    PopulateBanner, PopulateCategory,
    PopulateCoupons, PopulateProduct,
    PopulateBrand
)
from .models import User, nodify
from django.contrib.auth.models import Group


def freshStart():
    root = User.objects.create(
        username="root",
        email="phishink5@gmail.com",
        is_superuser=True,
        is_staff=True
    )
    root.set_password("Hood@roo1")
    customer = Group.objects.create(name="customer")
    root.groups.add(customer)
    root.save()
    nodify(root)
    PopulateBanner().totally_random(15)
    PopulateCoupons().totally_random(30)
    PopulateBrand().totally_random(25)
    PopulateCategory().totally_random(50)
    PopulateProduct().totally_random(200)
    return "OK"
