from shop.models import Category, Product, SubCategory, Banner
from core.models import AddressAndInfo, Profile
import random
from string import ascii_letters
import os
import sys
from essential_generators import DocumentGenerator as gen
from datetime import timedelta
from django.utils import timezone
from ecom.settings import BASE_DIR
import os

gen = gen()
gen.init_word_cache()
gen.init_sentence_cache()


class PopulateionError(Exception):
    pass


class Random:
    @staticmethod
    def random(**kwargs):
        random_dict = {}
        for kwarg in kwargs:
            objects = kwargs[kwarg].objects.all()
            if not objects:
                raise PopulationError(f"Populate {title(kwarg)}.")
            random_dict[kwarg] = random.choice(objects)
        return random_dict

    @staticmethod
    def Charfield(max_length, prefix="sample"):
        chars = list(ascii_letters)
        random.shuffle(chars)
        suggested = prefix + "".join(chars)
        chosen = ""
        for i in range(random.randint(0, max_length)):
            chosen += suggested[i]
        return chosen

    @staticmethod
    def FloatField(Max=None, Min=None):
        suggested = float(random.randint(
            Min or random.randint(1, 30), Max or random.randint(31, 100)
        ) / random.randint(20, 29))
        return suggested

    @staticmethod
    def SlugField():
        return gen.slug()

    @staticmethod
    def ImageField(folder_path):
        import re
        images = []
        for img in os.listdir(folder_path):
            if re.search(r"png|jpeg|jpg", img):
                images.append(img)
        if not images:
            raise PopulationError("Directory not populated with images.")
        return random.choice(images)

    @staticmethod
    def BooleanField():
        return random.choice([True, False])

    @staticmethod
    def TextField():
        return gen.sentence()

    @staticmethod
    def DateTimeField(*args, method="add"):
        kwargs = {
            arg: gen.small_int() for arg in args
        }
        if method == "add":
            return timezone.now() + timedelta(**kwargs)
        return timezone.now() - timedelta(**kwargs)


class Populate:
    model = None

    def init(self, **kwargs):
        new = self.model.objects.create(**kwargs)
        new.save()

    def destroy(self, number):
        objects = self.model.objects.all()[:number]
        for obj in objects:
            obj.delete()


class PopulateProduct(Populate):
    """
    You would need to populate Product and SubCategory
    else an error would be raised
    Populate Products with random data

    """
    model = Product

    def __init__(
            self,
            number: int,
    ):
        for i in range(number):
            kwargs = dict(
                name=Random.Charfield(45, "Product"),
                price=Random.FloatField(100, 10),
                slug=Random.SlugField(),
                image=Random.ImageField(os.path.join(BASE_DIR, "media")),
                featured=Random.BooleanField(),
                top_product=Random.BooleanField(),
                category=Random.random(cat=Category)["cat"],
                sub_category=Random.random(sub=SubCategory)["sub"],
                discount=Random.FloatField(100, 10),
                discounted_price=Random.FloatField(100, 10)
            )
            super().init(**kwargs)


class PopulateCategory(Populate):
    model = Category

    def __init__(self, number):
        for i in range(number):
            kwargs = dict(
                name=Random.Charfield(45, "Category"),
                slug=Random.SlugField()
            )
            super().init(**kwargs)


class PopulateSubCategory(Populate):
    model = SubCategory

    def __init__(self, number):
        for i in range(number):
            kwargs = dict(
                name=Random.Charfield(45, "SubCategory"),
                slug=Random.SlugField(),
                parent=Random.random(cat=Category)["cat"]
            )
            super().init(**kwargs)


class PopulateBanner(Populate):
    model = Banner

    def __init__(self, number):
        for i in range(number):
            kwargs = dict(
                image=Random.ImageField(os.path.join(BASE_DIR, "banners")),
                message=Random.TextField(),
                expiry_date=Random.DateTimeField("minutes", "hours")
            )
            super().init(**kwargs)
