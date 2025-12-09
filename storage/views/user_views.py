from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from storage.models import Transaction
from django.core.paginator import Paginator
from django.db.models import Q


@login_required(login_url="items:login")
def user_profile(request, user_id):
    """
    View to display user details.

    Requires a logged user. Fetches the User object securely by 'user_id'.
    Retrieves all associated Transaction objects (where the user is involved as borrower or lender),
    orders them descendingly by 'loan_date', and applies pagination (17 items per page).

    Parameters:
    ----------
    request : HttpRequest
        The HttpRequest object.
    user_id : int
        The primary key used to fetch in DB the object selected.
    Returns:
    -------
    HttpResponse:
        -Renders 'storage/user_profile.html' and loads the context with the user data and the transactions (GET).
    """

    single_user = User.objects.filter(pk=user_id).first()

    transaction = Transaction.objects.filter(
        Q(from_user=user_id) | Q(to_user=user_id)
    ).order_by("-loan_date")

    paginator = Paginator(transaction, 17)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "single_user": single_user,
        "page_obj": page_obj,
        "site_title": "User Profile - ",
    }

    return render(request, "storage/user_profile.html", context)
