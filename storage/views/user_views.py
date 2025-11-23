from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required(login_url="items:login")
def user_profile(request, user_id):

    single_user = User.objects.filter(pk=user_id).first()

    context = {"user": single_user, "site_title": "User Profile - "}

    return render(request, "storage/user_profile.html", context)


@login_required(login_url="items:login")
def user_owner_profile(request):

    profile_user = request.user

    context = {"profile_user": profile_user, "site_title": "User Profile - "}

    return render(request, "storage/user_profile.html", context)
