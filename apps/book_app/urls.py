from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^books$', views.books),
    url(r'^add_book$', views.add_book),
    url(r'^book_review$', views.book_review),
    url(r'^book/(?P<id>\d+)$', views.book),
    url(r'^review/(?P<id>\d+)$', views.review),
]