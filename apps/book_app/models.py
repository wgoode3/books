from __future__ import unicode_literals
from django.db import models
from ..user_app.models import User

class ReviewManager(models.Manager):
    def new_book_and_review(self, post_data, user):
        print post_data, user

        response = {
            "errors": [],
            "valid": True
        }

        if post_data["author"] == "Other":
            if len(post_data["other"]) < 1:
                response["valid"] = False
                response["errors"].append("Author is required")
            else:
                author = Author.objects.create(name=post_data["other"])
                author_id = author.id
        else:
            author_id = post_data["author"]

        if len(post_data["title"]) < 1:
            response["valid"] = False
            response["errors"].append("Title is required")
        else:
            book = Book.objects.create(title=post_data["title"], author_id=author_id)

        if response["valid"]:
            review = Review.objects.create(review=post_data["review"], rating=post_data["rating"], reviewer_id=user, book=book)

        return response

    def new_review(self, post_data, user, book):
        if len(Review.objects.filter(reviewer_id=user).filter(book_id=book)) == 0:
            Review.objects.create(review=post_data["review"], rating=post_data["rating"], reviewer_id=user, book_id=book)
            return True
        else:
            return False

class Author(models.Model):
    name = models.CharField(max_length=255)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books")

class Review(models.Model):
    rating = models.IntegerField()
    review = models.TextField(max_length=1000)
    reviewer = models.ForeignKey(User, related_name="reviews")
    book = models.ForeignKey(Book, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add = True)

    objects = ReviewManager()