from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from storage.forms import RegisterForm, RegisterUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth


def register(request):
    """
    View register new users.

    Initializes RegisterForm. Handles POST submission by validating the data and saving
    the new user object if validation succeeds.

    Parameters:
    ----------
    request : HttpRequest
        The HttpRequest object. Used to retrieve data about the context.
    Returns:
    -------
    HttpResponse:
        -Redirects to 'items:login' if the form validation succeeds (POST).
        -Renders 'storage/register.html' and loads the context and the site_title (GET)
    """
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "User registered successfully!")
            return redirect("items:login")

    return render(
        request,
        "storage/register.html",
        {"form": form, "template_name": "register.html"},
    )


@login_required(login_url="items:login")
def user_update(request):
    """
    View to update user data.

    Requires a logged user. Initializes RegisterUpdateForm with the logged user's instance
    for pre-population. Handles POST submission by validating the data and saving the
    updated user object if validation succeeds.

    Parameters:
    ----------
    request : HttpRequest
        The HttpRequest object.
    Returns:
    -------
    HttpResponse:
        -Renders 'storage/user_update.html' with the form pre-populated with user data (GET).
        -Renders 'storage/user_update.html' with the form and validation errors (Invalid POST).
        -Rendirects to 'items:user_update' after successful update (Valid POST).
    """
    form = RegisterUpdateForm(instance=request.user)

    if request.method != "POST":
        return render(request, "storage/user_update.html", {"form": form})

    form = RegisterUpdateForm(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(request, "storage/user_update.html", {"form": form})

    form.save()
    messages.success(request, "User updated sucessfully!")

    return redirect("items:user_update")


def login_view(request):
    """
    View to login a existent user.

    Initializes AuthenticationForm. Handles POST submission by validating the data,
    authenticating the user, and logging them in if validation succeeds.
    If the user is already authenticated, they are redirected to the index page..

    Parameters:
    ----------
    request : HttpRequest
        The HttpRequest object.
    Returns:
    -------
    HttpResponse:
        -Rendirects to 'items:index' after successful login (Valid POST).
        -Renders 'storage/login.html' with error message if validation fails (POST).
        -Renders 'storage/login.html' with the empty AuthenticationForm (GET).
    """
    form = AuthenticationForm(request)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            messages.success(request, "Logged Successfully")
            user = form.get_user()
            auth.login(request, user)
            return redirect("items:index")
        else:
            messages.error(request, "Login or password are incorrect")

    return render(
        request, "storage/login.html", {"form": form, "template_name": "login.html"}
    )


@login_required(login_url="items:login")
def logout_view(request):
    """
    View to logut the logged user.

    Handles session termination by calling auth.logout(request). This action
    should be accessed via POST for security (CSRF protection).

    Parameters:
    ----------
    request : HttpRequest
        The HttpRequest object.
    Returns:
    -------
    HttpResponse:
        -Rendirects to 'items:login' after successful logout (Valid POST).
        -Redirects to 'items:user_profile' if the method is not POST (Security check).
    """
    if request.method == "POST":
        auth.logout(request)
        return redirect("items:login")

    return redirect("items:user_profile", user_id=request.user.id)
