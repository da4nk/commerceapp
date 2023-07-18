from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("CreateListing", views.create, name = "create"),
    path("Auction_listing/<str:title>", views.auction_listings, name ="auction_listings"),
    path("Categories", views.categories, name = "categories"),
    path("Categories/<str:title>", views.cdirect, name = "cdirect"),
    path("Closed Listings", views.closed, name ="closed"),
    path("Closed_auction/<str:title>", views.old_auction, name = "old_auction"),
    path("watchlist/<str:title>", views.watchlist, name = "watchlist"),
    path("YourWatchList", views.watched_items, name = "watched_items"),
    path('comments/<str:id>', views.comment, name= "comments")
]
