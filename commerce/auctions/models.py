from django.contrib.auth.models import AbstractUser
from django.db import models

# Define a custom user model that extends AbstractUser
class User(AbstractUser):
    pass

# Define a model for item bids
class Bid(models.Model):
    # Field to store the bid amount
    bid = models.IntegerField(default=0)
    # Field to store the user who placed the bid
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")

# Define a model for item categories
class Category(models.Model):
    # Field to store the name of the category
    categoryName = models.CharField(max_length=50)

    # Method to return the name of the category as a string
    def __str__(self):
        return self.categoryName


# Define a model for auction listings
class Listing(models.Model):
    # Field to store the title of the listing
    title = models.CharField(max_length=30)
    # Field to store the description of the listing
    description = models.CharField(max_length=300)
    # Field to store the URL of the image associated with the listing
    imageUrl = models.CharField(max_length=1000)
    # Field to store the highest bid for the item
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    # Field to indicate whether the auction is still active
    isActive = models.BooleanField(default=True)
    # Field to store the user who created the listing
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    # Field to store the category associated with the listing
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="Cateogry")
    # Field to store the users who have added the listing to their watchlist
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingWatchlist")

    # Method to return the title of the listing as a string
    def __str__(self):
        return self.title

# Define a model for comments on auction listings
class Comment(models.Model):
    # Field to store the user who wrote the comment
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userComment")
    # Field to store the listing the comment was made on
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listingComment")
    # Field to store the message of the comment
    message = models.CharField(max_length=200)

    # Method to return a string representation of the comment
    def __str__(self):
        return f"{self.author} commented on {self.listing}"


