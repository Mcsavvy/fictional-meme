from globals.models import (
    Contact, Product, Category, Brand, Categories,
    Brands
)
from django.views.decorators.cache import cache_page
from globals import render
from globals.utils import grid
from globals.query import Query
# Create your views here.


@cache_page(None)
def index(request):
    if request.GET.get("query"):
        query = request.GET.get("query")
        cat = request.GET.get("cat")
        if cat not in Categories().all_names:
            cat = None
        brand = request.GET.get("brand")
        if brand in Categories().all_names:
            brand = Brand.objects.get(name=brand)
        else:
            brand = None
        query = Query(query)
        filters = {}
        if brand:
            filters['brand'] = brand
        if cat:
            filters['categories_name'] = cat
        query.models = {
            "model": Product,
            "alias": "products",
            "search": ["name"],
            "return": ["url", "name", "image"],
            "filter": filters,
            "order": ["name"]
        }
        query.models = {
            "model": Category,
            "alias": "categories",
            "search": ["name"],
            "return": ["url", "name", "image"]
        }
        query.models = {
            "model": Brand,
            "alias": "brands",
            "search": ["name"],
            "return": ["url", "name", "image"]
        }
        context = {
            "query": query.resolve() or None
        }
        return render(request, "main/search.html", context)

    featured = Product.objects.filter(featured=True, top_product=False)
    top_product = Product.objects.filter(top_product=True, featured=False)
    context = {
        'featured': grid(
            featured,
            6,
            slide=int(request.GET.get("fslide", 1)),
            loop=True,
            shuffle=True
        ),
        'top_product': grid(
            top_product,
            6,
            slide=int(request.GET.get("tslide", 1)),
            loop=True,
            shuffle=True
        )
    }
    # messages.info(request, "INFO")
    # messages.warning(request, "WARNING")
    # messages.error(request, "ERROR")
    # messages.success(request, "SUCCESS")
    return render(request, 'main/index.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )
    return render(request, 'main/contact.html')

