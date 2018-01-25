from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login(self, email, password):

        response = {
            "errors": [],
            "user": None,
            "valid": True
        }

        if len(email) < 1:
            response["valid"] = False
            response["errors"].append("Email is required")
        elif not EMAIL_REGEX.match(email):
            response["valid"] = False
            response["errors"].append("Invalid Email")
        else:
            list_of_emails = User.objects.filter(email=email.lower())
            if len(list_of_emails) == 0:
                response["valid"] = False
                response["errors"].append("Email does not exist")
        if len(password) < 8:
            response["valid"] = False
            response["errors"].append("Password must be 8 characters or more")

        if response["valid"]:
            if bcrypt.checkpw(password.encode(), list_of_emails[0].password.encode()):
                response["user"] = list_of_emails[0]
            else:
                response["valid"] = False
                response["errors"].append("Incorrect Password")

        return response

    def register(self, name, alias, email, password, confirm_password):

        response = {
            "errors": [],
            "user": None,
            "valid": True
        }

        if len(name) < 1:
            response["valid"] = False
            response["errors"].append("Name is required")
        if len(alias) < 1:
            response["valid"] = False
            response["errors"].append("Alias is required")
        if len(email) < 1:
            response["valid"] = False
            response["errors"].append("Email is required")
        elif not EMAIL_REGEX.match(email):
            response["valid"] = False
            response["errors"].append("Invalid Email")
        else:
            list_of_emails = User.objects.filter(email=email.lower())
            if len(list_of_emails) > 0:
                response["valid"] = False
                response["errors"].append("Email already exists")
        if len(password) < 8:
            response["valid"] = False
            response["errors"].append("Password must be 8 characters or more")
        if confirm_password != password:
            response["valid"] = False
            response["errors"].append("Password must match Confirm Password")

        if response["valid"]:
            response["user"] = User.objects.create(
                name=name,
                alias=alias,
                email=email.lower(),
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            )

        return response

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()