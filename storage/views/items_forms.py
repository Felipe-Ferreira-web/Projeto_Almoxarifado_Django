from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from storage.forms import ItemForm
from storage.models import Item


@login_required(login_url="items:login")
def create(request):
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
    item = get_object_or_404(Item, pk=item_id)

    form_action = reverse("items:update", args=(item_id,))

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
    item = get_object_or_404(Item, pk=item_id)

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
