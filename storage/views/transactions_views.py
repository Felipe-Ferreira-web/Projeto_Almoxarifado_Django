from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from storage.models import Item, Transaction
from django.core.paginator import Paginator
from django.contrib import messages


@login_required(login_url="items:login")
def Transactions(request):
    """
    View to display transaction objects from the Transaction class.

    Requires a logged user. Fetches all Transaction objects and orders them descendingly by '-id'. Use Paginator to separate the objects into 17 elements per page and use request.get to select a page.
    Then attributes the pages to page_obj and retrives the value with context.

    Parameters:
    -----------
    request : HttpRequest
        The HttpRequest object. Used to retrieve the page number for the pagination parameter("page") from the query string.

    Returns:
    --------
    HttpResponse:
        -Renders 'storage/transactions.html' and loads the context and site_title (GET)
    """
    transaction = Transaction.objects.order_by("-id")

    paginator = Paginator(transaction, 17)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "site_title": "Transactions - "}

    return render(request, "storage/transactions.html", context)


@login_required(login_url="items:login")
def ItemTransaction(request, item_id):
    """
    View to handle Item Loans and Devolutions.

    Requires a logged user and only accepts the POST method for transactions.
    The action is determined by the item's current availability (item.is_available).

    Flow:
    -----
    1. LOAN (If item.is_available is True): Creates a LOAN transaction, sets item.is_available=False, and saves status.
    2. DEVOLUTION (If item.is_available is False): Finds the active LOAN transaction by the current user.
    If found and user matches active loan recipient, creates a DEVOLUTION transaction, sets item.is_available=True, and saves status.

    Parameters:
    -----------
    request : HttpRequest
        The HttpRequest object. Used to retrieve current transaction data.
    item_id : int
        The primary key used to fetch in DB the object selected

    Returns:
    --------
    HttpResponse:
        -Redirects to 'items:index' if the request method is not POST (Integrity Check).
        -Redirects to 'items:item' if the Loan Transaction succeed.
        -Redirects to 'items:item' if the Devolution Transaction succeed.
        -Redirects to 'items:index' if Devolution fails.
    """

    if request.method != "POST":
        return redirect("items:index", user_id=request.user.id)

    item = get_object_or_404(Item, pk=item_id)

    if item.is_available:
        Transaction.objects.create(
            item=item,
            from_user=item.owner,
            to_user=request.user,
            was_available=False,
            type=Transaction.LOAN,
        )

        item.is_available = False

        item.save()

        messages.success(request, "Loan succeeded!")
        return redirect("items:item", item_id=item_id)

    else:
        active_loan = (
            Transaction.objects.filter(
                item=item, to_user=request.user, type=Transaction.LOAN
            )
            .order_by("-loan_date")
            .first()
        )

        if active_loan and active_loan.to_user == request.user:

            Transaction.objects.create(
                item=item,
                from_user=request.user,
                to_user=item.owner,
                was_available=item.is_available,
                type=Transaction.DEVOLUTION,
            )

            item.is_available = True
            item.save()

            messages.success(request, "Devolution succeeded!")
            return redirect("items:item", item_id=item_id)

    return redirect("items:user_profile", user_id=request.user.id)
