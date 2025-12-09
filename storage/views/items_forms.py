from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from storage.forms import ItemForm
from storage.models import Item


@login_required(login_url="items:login")
def create(request):
    """
    View to create an Item

    Require a logged user. Receives data from  user through a ItemForm form and assign the item to the user logged as the owner.

    Parameters:
    ----------
    request : HttpRequest
        The object Request contains metadata from the POST Method from form.

    Returns:
    -------
    HttpResponse:
        -Redirects to 'items:update' if successful (valid POST)
        -Renders 'storage/update.html' if form is invalid (invalid POST)
        -Render 'storage/create' if form is empty (GET)
    """

    form_action = reverse("items:create")

    if request.method == "POST":
        form = ItemForm(request.POST)

        context = {"form": form, "form_action": form_action}

        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            return redirect("items:update", item_id=item.pk)

        return render(request, "storage/update.html", context)

    context = {"form": ItemForm(), "form_action": form_action}

    return render(request, "storage/create.html", context)


@login_required(login_url="items:login")
def update(request, item_id):
    """
    View to update an Item

    Require a logged user. Retrieves the Item object using item_id to populate the form. Checks if the logged user is the same as the owner of the item.
    After receiving a POST method checks if the form is valid and if the validation succeed the items's data will be replaced.

    Parameters:
    ----------
    request :  HttpRequest
        The object Request containing metadata and form submission data.
    item_id (int) :
        The primary key used to fetch the Item object to be updated.

    Returns:
    -------
    HttpResponse:
        -Redirects to 'items:index' if owner verifications fail(Security Check)
        -Redirects to 'items:update' if successful (valid POST)
        -Renders 'storage/update.html' if form is invalid (invalid POST)
        -Render 'storage/update' with the item's current data (GET)
    """

    item = get_object_or_404(Item, pk=item_id)

    form_action = reverse("items:update", args=(item_id,))

    if request.user != item.owner:
        return redirect("items:index")

    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)

        context = {"form": form, "form_action": form_action, "item": item}

        if form.is_valid():
            item = form.save()
            return redirect("items:update", item_id=item.pk)

        return render(request, "storage/update.html", context)

    context = {
        "form": ItemForm(instance=item),
        "form_action": form_action,
        "item": item,
    }

    return render(request, "storage/update.html", context)


@login_required(login_url="items:login")
def delete(request, item_id):
    """
    View to delete an Item

    Require a logged user. Checks if the logged user is the same as the owner of the item. Deletes through POST, while awaits for 'confirmation' key with value 'yes

    Parameters:
    ----------
    request : HttpRequest
        The object Request containing metadata about object.
    item_id (int):
        The primary key used to fetch the Item object to be deleted.

    Returns:
    -------
    HttpResponse:
        -Redirects to 'items:index' if owner verifications fail(Security Check)
        -Redirects to 'items:index' if confirmation == 'yes' after deleting Item (POST)
        -Renders 'storage/item' with the item's current data and the value of confirmation (POST)
    """
    item = get_object_or_404(Item, pk=item_id)

    if request.user != item.owner:
        return redirect("items:index")

    confirmation = request.POST.get("confirmation", "no")

    if confirmation == "yes":
        item.delete()
        return redirect("items:index")

    return render(
        request,
        "storage/item.html",
        {
            "item": item,
            "confirmation": confirmation,
        },
    )
