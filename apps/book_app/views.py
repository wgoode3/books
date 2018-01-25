## encoding:utf-8--
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Author, Book, Review

def books(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must log in first!')
        return redirect("/")

    reviews = []
    for r in Review.objects.all().order_by("-id")[:3]:
        reviews.append({
            "title": r.book.title,
            "rating": r.rating,
            "review": r.review,
            "reviewer": r.reviewer.name,
            "created_at": r.created_at,
            "stars": "★"*int(r.rating) + "☆"*(5-int(r.rating))
        })

    data = {
        'user': User.objects.get(id=request.session["user_id"]),
        'books': Book.objects.all(),
        'reviews': reviews
    }

    return render(request, "book_app/index.html", data)

def add_book(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must log in first!')
        return redirect("/")
    authors = Author.objects.all()
    return render(request, "book_app/add.html", {"authors": authors})

def book_review(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must log in first!')
        return redirect("/")
    response = Review.objects.new_book_and_review(request.POST, request.session["user_id"])
    print(response)
    return redirect("/books")

def book(request, id):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must log in first!')
        return redirect("/")
    book = Book.objects.get(id=id)
    return render(request, "book_app/book.html", {"book": book})

def review(request, id):
    response = Review.objects.new_review(request.POST, request.session["user_id"], id)
    print response
    return redirect("/books")