from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("CreateListing", views.create, name = "create"),
    path("Auction_listing/<str:title>", views.auction_listings, name ="auction_listings")
]
