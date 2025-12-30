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

    Requires a logged-in user and only accepts POST requests. The action is
    determined by the item's current availability, and the state is managed
    by updating the 'current_loan' foreign key on the Item model.

    Flow:
    -----
    1. LOAN (If item.is_available is True):
        - Creates a LOAN transaction record.
        - Sets item.is_available to False.
        - Maps item.current_loan to the newly created transaction.
        - Saves the item state.

    2. DEVOLUTION (If item.is_available is False):
        - Verifies if the 'current_loan' exists and if the logged-in user
        matches the current borrower (to_user).
        - Creates a DEVOLUTION transaction record.
        - Sets item.is_available to True.
        - Clears item.current_loan (sets to NULL).
        - Saves the item state.

    Parameters:
    -----------
    request : HttpRequest
        The HttpRequest object containing user and method data.
    item_id : int
        The primary key of the Item to be transacted.

    Returns:
    --------
    HttpResponse:
        - Redirects to 'items:index' if the request method is not POST.
        - Redirects to 'items:item' upon successful Loan or Devolution.
        - Redirects to 'items:user_profile' with an error message if the user lacks permission to return the item.
    """

    if request.method != "POST":
        return redirect("items:index")

    item = get_object_or_404(Item, pk=item_id)

    if item.is_available:
        new_loan = Transaction.objects.create(
            item=item,
            from_user=item.owner,
            to_user=request.user,
            was_available=True,
            type=Transaction.LOAN,
        )

        item.is_available = False
        item.current_loan = new_loan
        item.save()

        messages.success(request, "Loan succeeded!")
        return redirect("items:item", item_id=item_id)

    else:
        if item.current_loan and item.current_loan.to_user == request.user:

            Transaction.objects.create(
                item=item,
                from_user=request.user,
                to_user=item.owner,
                was_available=item.is_available,
                type=Transaction.DEVOLUTION,
            )

            item.is_available = True
            item.current_loan = None
            item.save()

            messages.success(request, "Devolution succeeded!")
            return redirect("items:item", item_id=item_id)
        else:
            messages.error(request, "You are not allowed to return this item.")

    return redirect("items:user_profile", user_id=request.user.id)
