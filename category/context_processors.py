from os import link
from .models import Category

# To use this anywhere in our templates


def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
