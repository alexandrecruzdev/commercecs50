from django.contrib import admin
from .models import Auction, Bid, Comment, User,Watchlist
# Register your models here.

admin.site.register(Auction)

admin.site.register(Bid)

admin.site.register(Comment)

admin.site.register(User)

admin.site.register(Watchlist)