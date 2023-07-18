from django.contrib import admin
from .models import User, listings, Bids, Comments, closed_listings, WatchList
# Register your models here.

class ListingsAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "price", "category", "date", "winner")

class ClosedListingsAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "price", "category", "date", "winner")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ("content", "auction")

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "balance")

class BidsAdmin(admin.ModelAdmin):
    list_display = ("amount", "auction", "user")

class WatchListAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "added")

admin.site.register(listings, ListingsAdmin)
admin.site.register(closed_listings, ClosedListingsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Bids, BidsAdmin)
admin.site.register(WatchList, WatchListAdmin)
