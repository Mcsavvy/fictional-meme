import os
import sys
import re
from string import ascii_letters, Template
import random
from datetime import datetime, timedelta
from django.utils import timezone
from PIL import Image, ImageDraw
from ecom.settings import BASE_DIR, MEDIA_ROOT
from essential_generators import DocumentGenerator as generator


class PopulationError(Exception):
    pass


class CachedObject:
    def __init__(self, name, **_):
        self.key = name

    def get(self, default=None, **_):
        if not getattr(self, "_value", None):
            if default:
                setattr(self, "_value", default)
                return default
            return default
        return getattr(self, "_value")


bucket = CachedObject('bucket')


class Random:
    @staticmethod
    def randomFields(**kwargs):
        random_dict = {}
        for kwarg in kwargs:
            objects = kwargs[kwarg].objects.all()
            if not objects:
                raise PopulationError(f"Populate {kwarg.title()}.")
            random_dict[kwarg] = random.choice(objects)
        return random_dict

    @staticmethod
    def random(model):
        objects = model.objects.all()
        if not objects:
            raise PopulationError(f"Populate {str(model)}.")
        return random.choice(objects)

    @staticmethod
    def Charfield(max_length, prefix="sample"):
        chars = list(ascii_letters)
        random.shuffle(chars)
        suggested = "".join(chars)
        chosen = ""
        for i in range(random.randint(0, max_length)):
            chosen += suggested[i]
        return prefix + chosen

    @staticmethod
    def FloatField(Max=None, Min=None):
        suggested = float(random.randint(
            Min or random.randint(1, 30), Max or random.randint(31, 100)
        ) / random.randint(10, 100))
        return suggested

    @staticmethod
    def SlugField():
        if not bucket.get():
            buck = generator()
            buck.init_word_cache()
            buck.init_sentence_cache()
            bucket.get(buck, timeout=None)
        return bucket.get().slug()

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
        if not bucket.get():
            buck = generator()
            buck.init_word_cache()
            buck.init_sentence_cache()
            bucket.get(buck, timeout=None)
        return bucket.get().sentence()

    @staticmethod
    def DateTimeField(*args, method="add"):
        if not bucket.get():
            buck = generator()
            buck.init_word_cache()
            buck.init_sentence_cache()
            bucket.get(buck, timeout=None)
        kwargs = {
            arg: bucket.get().small_int() for arg in args
        }
        if method == "add":
            return timezone.now() + timedelta(**kwargs)
        return timezone.now() - timedelta(**kwargs)

    @staticmethod
    def BlankImage(**settings):
        _settings = dict(
            colour="#FFFFFF",
            size=(300, 300),
            text="",
            text_colour="#000000",
            text_position=(140, 140),
            path=MEDIA_ROOT,
            name=Random.Charfield(10, "img:") + ".png"
        )
        _settings.update(settings)
        img = Image.new(
            "RGB",
            _settings['size'],
            color=_settings['colour']
        )
        if _settings['text']:
            draw = ImageDraw.Draw(img)
            draw.text(
                _settings['text_position'],
                str(_settings['text']),
                _settings['text_colour']
            )
        img.save(os.path.join(
            _settings['path'], _settings['name']
        ))
        return _settings['path'], _settings['name']

    @staticmethod
    def UrlField():
        if not bucket.get():
            buck = generator()
            buck.init_word_cache()
            buck.init_sentence_cache()
            bucket.get(buck, timeout=None)
        return bucket.get().url()
