from django.contrib import admin
from .models import *
# Register your models here.
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ['id','name','price','owner','description','category','image','time','status']

class BidAdmin(admin.ModelAdmin):
    list_display = ['user','auction_listing','bid_price','time','winning']
class CommentAdmin(admin.ModelAdmin):
    list_display= ['user','auction_listing','time','content']


admin.site.register(User)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid,BidAdmin)
admin.site.register(Comment, CommentAdmin)