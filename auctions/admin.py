from django.contrib import admin
from auctions.models import Listing, User

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
