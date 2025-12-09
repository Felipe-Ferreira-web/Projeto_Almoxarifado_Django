from django.shortcuts import render, redirect
from django.db.models import Q
from storage.models import Item
from django.core.paginator import Paginator


def index(request):
    """
    View to display the objects from Item class.

    Fetches all Item objects and orders them descendingly by '-item_id'. Use Paginator to separate the objects into 17 elements per page and use request.get to select a page.
    Then attributes the pages to page_obj and retrives the value with context.

    Parameters:
    -----------
    request : HttpRequest
        The HttpRequest object. Used to retrieve the page number for the pagination parameter("page") from the query string.

    Returns:
    --------
    HttpResponse:
        -Renders 'storage/index.html' and loads the context and site_title (GET)
    """
    items = Item.objects.order_by("-item_id")

    paginator = Paginator(items, 17)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "site_title": "Items - "}

    return render(request, "storage/index.html", context)


def item(request, item_id):
    """
    View to display data about a single item.

    Fetch Item objects by item_id and select the first object to assign to the context.

    Parameters:
    ----------
    request : HttpRequest
        The HttpRequest object. Used to retrieve data about the context.
    item_id (int) :
        The primary key used to fetch in DB the object selected.
    Returns:
    -------
    HttpResponse:
        -Renders 'storage/item.html' and loads the context and the site_title (GET)
    """

    item = Item.objects.filter(pk=item_id).first()

    context = {
        "item": item,
        "site_title": "Item - ",
    }

    return render(request, "storage/item.html", context)


def search(request):
    """
    View to manage the search feature.

    Process the received data through GET. Evaluate if the value is not empty and filters by different standards.
    Use Paginator to separate the objects into 10 elements per page and use request.get to select a page.
    Then attributes the pages to page_obj with the search_value and retrives the value with context

    Parameters:
    ----------
    request : HttpRequest
        The HttpRequest object. Used to retrieve data inserted by the user.
    Returns:
    -------
    HttpResponse:
        -Redirect to 'items:index" if the value is empty (Data evaluation)
        -Renders 'storage/item.html' and loads the context with the paginated results ('page_obj'), site title, and the search term ('search_value').
    """
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

    paginator = Paginator(items, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "site_title": "Search - ",
        "search_value": search_value,
    }

    return render(request, "storage/index.html", context)
