from .models import (
    AddressAndInfo, Profile,
    Product, Coupon, Products,
    Category, Product, Banner,
    Brand
)
from .random_fields import Random
import os
import random
from ecom.settings import BASE_DIR


class PopulationError(Exception):
    pass


class Populate:
    model = None

    def init(self, **kwargs):
        new = self.model.objects.create(**kwargs)
        new.save()
        return new

    def destroy(self, number):
        objects = self.model.objects.all()[:number]
        for obj in objects:
            obj.delete()


class PopulateBrand(Populate):
    model = Brand

    def totally_random(self, number):
        for i in range(number):
            image = Random.BlankImage(
                name="Brand.png",
                colour='purple',
            )[1]
            kwargs = dict(
                image=image,
                description="This brand surprisingly depicts...",
                slug=Random.SlugField(),
                name=Random.Charfield(45, "Brand "),
            )
            super().init(**kwargs)


class PopulateBanner(Populate):
    model = Banner

    def totally_random(self, number):
        for i in range(number):
            image = Random.BlankImage(
                name=Random.Charfield(10, "slide ") + ".png",
                colour=random.choice(
                    ["black", "blue", "red", "green", "orange", "grey"]
                ),
                size=(4000, 2000)
            )[1]
            kwargs = dict(
                image=image,
                message=Random.TextField(),
                expiry_date=Random.DateTimeField("minutes", "hours"),
                link=Random.UrlField(),
            )
            super().init(**kwargs)


class PopulateCategory(Populate):
    model = Category

    def totally_random(self, number):
        for i in range(number):
            try:
                parent = Random.random(Category)
            except Exception:
                parent = None
            kwargs = dict(
                name=Random.Charfield(45, "Category"),
                slug=Random.SlugField(),
                image=Random.BlankImage(
                    name="Category.png",
                    colour="lime"
                )[1],
            )
            if parent:
                kwargs['parent'] = parent
            super().init(**kwargs)


class PopulateCoupons(Populate):
    model = Coupon

    def totally_random(self, number):
        for i in range(number):
            kwargs = dict(
                code=Random.Charfield(15, "COUPON"),
                discount=Random.FloatField(1000, 100),
                expire=Random.DateTimeField("days")
            )
            super().init(**kwargs)


class PopulateProduct(Populate):
    model = Product

    def smart_random(self, number):
        for i in range(number):
            image = Random.ImageField(os.path.join(BASE_DIR, "products"))
            parsed = self.parser(image)
            category = Category.objects.get(id=parsed['cat'])
            name = parsed["name"]
            if name in Products().all_names:
                continue
            kwargs = dict(
                name=name,
                price=Random.FloatField(100, 10),
                slug=Random.SlugField(),
                image=image,
                featured=Random.BooleanField(),
                top_product=Random.BooleanField(),
                discount=Random.FloatField(100, 10),
                brand=Random.random(Brand)
            )
            new = super().init(**kwargs)
            new.categories.add(category)
            new.save()

    def totally_random(self, number):
        for i in range(number):
            kwargs = dict(
                name=Random.Charfield(max_length=20, prefix="Product "),
                price=Random.FloatField(10000, 100),
                slug=Random.SlugField(),
                image=Random.BlankImage(name="Product.png")[1],
                featured=Random.BooleanField(),
                top_product=Random.BooleanField(),
                discount=Random.FloatField(1000, 10),
            )
            category = Random.random(Category)
            new = super().init(**kwargs)
            new.categories.add(category)
            new.save()

    def parser(self, file_name):
        _ = {}
        _["folder"], _["file"] = os.path.split(file_name)
        _["plain"], _["ext"] = os.path.splitext(_["file"])
        args = _['plain'].split(":")
        if not args:
            raise Exception("parser could not parse image::{0}".format(locals))
        if len(args) == 1:
            _["name"] = args[0]
        elif len(args) == 2:
            _["name"], _['cat'] = args
        elif len(args) >= 3:
            _['name'], _['cat'], _['par'], _['extras'] = args
        return _
