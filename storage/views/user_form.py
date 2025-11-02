from django.shortcuts import render, redirect
from storage.forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth


def register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Usuário Registrado")
            return redirect("items:login")

    return render(request, "storage/register.html", {"form": form})


def login_view(request):
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

    return render(request, "storage/login.html", {"form": form})


def logout_view(request):
    auth.logout(request)
    return redirect("items:login")
