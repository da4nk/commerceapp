from django.contrib import admin
from .models import User, listings, Bids, Comments, closed_listings
# Register your models here.
admin.site.register(User)
admin.site.register(listings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(closed_listings)