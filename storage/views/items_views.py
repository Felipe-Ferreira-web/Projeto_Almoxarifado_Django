from django.shortcuts import render, get_list_or_404, redirect
from django.db.models import Q
from storage.models import Item
from django.core.paginator import Paginator


def index(request):

    items = Item.objects.order_by("-item_id")

    paginator = Paginator(items, 17)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "site_title": "Items - "}

    return render(request, "storage/index.html", context)


def item(request, item_id):

    single_item = Item.objects.filter(pk=item_id).first()

    context = {"item": single_item, "site_title": "Item - "}

    return render(request, "storage/item.html", context)


def search(request):

    search_value = request.GET.get("q", "").strip()

    if search_value == "":
        return redirect("items:index")

    items = Item.objects.filter(
        Q(item_id__icontains=search_value)
        | Q(object__icontains=search_value)
        | Q(owner_id__username__icontains=search_value)
        | Q(description__icontains=search_value)
        | Q(storage_location__icontains=search_value)
        | Q(created_date__icontains=search_value)
    ).order_by("-item_id")

    context = {"items": items, "site_title": "Search - "}

    return render(request, "storage/index.html", context)
