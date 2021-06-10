# API requests handlers
# All views basically return json
from globals.models import User, Product
# from core.utils import render
from globals.query import Query
from django.http import JsonResponse
from random import choice

username_choices = list(
    range(10, 21)
) + list(
    range(100, 111)
) + list(
    range(2020, 2031)
)


def search(request, keyword):
    search = Query(keyword)
    search.models = {
        'model': Product,
        'alias': "products",
        'search': ["name"],
        'return': ["name", "slug"]
    }
    return JsonResponse(search.resolve(), safe=False)


def user_exists(request, username):
    try:
        User.objects.get(username=username)
        while True:
            try:
                suggested = username + str(choice(username_choices))
                User.objects.get(username=suggested)
            except User.DoesNotExist:
                break
        data = {
            "message": "Username '%s' already taken." % username,
            "level": "error",
            "suggested": suggested
        }
    except User.DoesNotExist:
        data = None
    print(data)
    return JsonResponse(data, safe=False)
