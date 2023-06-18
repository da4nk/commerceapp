from django.contrib import admin
from .models import User, listings, Bids, Comments
# Register your models here.
admin.site.register(User)
admin.site.register(listings)
admin.site.register(Bids)
admin.site.register(Comments)