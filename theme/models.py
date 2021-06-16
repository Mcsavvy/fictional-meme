from django.db import models


class Parse:
    """
    structure = 
    'arg1&&arg2&&args3??kwarg1=True&&kwarg2=False'
    """
    class Dict:
    def write_kwargs(**kwargs):



# Create your models here.
class Theme(models.Model):
    name = models.CharField(max_length=20, default='default')
    lt = models.CharField(max_length=20, default='#ffffff')
    dk = models.CharField(max_length=20, default='#161618')

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
