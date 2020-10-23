from django.contrib import admin
from auctions.models import Listing, User, Comment, Bid

# Register your models here.


class BidAdmin(admin.ModelAdmin):
    def item_title(self, obj):
        return obj.listing.item_title

    def bidding_user(self, obj):
        return obj.bidder.username
    list_display = ("item_title",
                    "bidding_user", "amount", "bidDate")


class CommentAdmin(admin.ModelAdmin):
    def item_title(self, obj):
        return obj.listing.item_title

    def comment_by(self, obj):
        return obj.commentBy.username

    list_display = ("item_title", "comment_by", "comment_title", "commentDate")


class ListingAdmin(admin.ModelAdmin):
    def created_by(self, obj):
        return obj.createdBy.username

    def current_highest_bid(self, obj):
        return obj.highestBid

    def auction_open(self, obj):
        if obj.auctionOpen:
            return 'Yes'
        else:
            return 'No'
    list_display = ('item_title', 'description', 'created_by',
                    'creationDate', 'category', 'current_highest_bid', 'auction_open')


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
