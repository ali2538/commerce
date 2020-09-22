from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f' username: {self.username} email: {self.email}'


class Listing(models.Model):
    """Model definition for listing."""

    # TODO: Define fields here
    name = models.CharField(max_length=512, default="Item", editable=True)
    description = models.TextField(
        max_length=1500, default='Item Description', editable=True)
    createdBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='lister')
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='winner', null=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    highestBid = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    startingBid = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=100)
    auctionOpen = models.BooleanField(default=True)
    item_image = models.CharField(max_length=2048)

    #     listingsID, createdBy, creationDate, highestBid, strartingBid, minimumRaise, category, auctionOpen, winner

    # class Meta:
    #     """Meta definition for listing."""

    #     verbose_name = 'listing'
    #     verbose_name_plural = 'listings'
    def __str__(self):
        return f'created by: {self.createdBy}, creationDate: {self.creationDate}, category: {self.category}'


class Bid(models.Model):
    listingId = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    bidDate = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    listingId = models.ForeignKey(Listing, on_delete=models.CASCADE)
    commentBy = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=5000)
    commentDate = models.DateTimeField(auto_now_add=True)


class WatchList(models.Model):
    listingID = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def __str__(self):
    #     pass

    # class Meta:
    #     db_table = ''
    #     managed = True
    #     verbose_name = 'WatchList'
    #     verbose_name_plural = 'WatchLists'
