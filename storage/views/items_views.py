from django.shortcuts import render
from storage.models import Item


def index(request):
    items = Item.objects.all()

    context = {
        "items": items,
    }

    return render(request, "storage/index.html", context)
