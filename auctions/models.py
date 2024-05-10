from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_listings')
    description = models.TextField()
    CATEGORY_CHOICES = [
        ('no_category_listed','No Category Listed'),
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home', 'Home'),
        # Add more choices as needed
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='No_Category_Listed')
    image = models.URLField()
    time = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)
    winning = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} : {self.winning} : {self.bid_price} : {self.auction_listing}: {self.id}'



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f'{self.user} commented {self.content} at {self.auction_listing} : {self.time}'

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='wishlisted')

    def __str__(self):
        return f"{self.user.username}'s Wishlist: {self.auction_listing.name}"