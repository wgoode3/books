from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

def index(request):
    return render(request, "user_app/index.html")

def register(request):
    response = User.objects.register(
        name=request.POST["name"],
        alias=request.POST["alias"],
        email=request.POST["email"],
        password=request.POST["password"],
        confirm_password=request.POST["confirm_password"]
    )
    if response["valid"]:
        messages.add_message(request, messages.SUCCESS, 'Welcome to the site!')
        request.session["user_id"] = response["user"].id
        return redirect("/books")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)

    return redirect("/")

def login(request):
    response = User.objects.login(
        email=request.POST["email"],
        password=request.POST["password"]
    )

    if response["valid"]:
        messages.add_message(request, messages.SUCCESS, 'Welcome to the site!')
        request.session["user_id"] = response["user"].id
        return redirect("/books")
    else:
        for error_message in response["errors"]:
            messages.add_message(request, messages.ERROR, error_message)

    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")
