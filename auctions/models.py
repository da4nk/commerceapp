from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone






class listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    image = models.URLField(default = "no image")
    price = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    category = models.CharField(default = "", max_length=20)
    date = models.DateTimeField(blank= True, default=timezone.now)
    winner = models.CharField(max_length = 64, default = "no winner")
    
    
    def __str__(self):

        return f" name of the item: {self.title}, description of item: {self.description}, image of item: {self.image}, cost of item: {self.price}, category the item is in: {self.category}, date: {self.date}"

class closed_listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    image = models.URLField(default = "no image")
    price = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    category = models.CharField(default = "", max_length=20)
    date = models.DateTimeField(blank= True, default=timezone.now)
    winner = models.CharField(max_length = 64, default = "no winner")
    
    
    def __str__(self):

        return f" name of the item: {self.title}, description of item: {self.description}, image of item: {self.image}, cost of item: {self.price}, category the item is in: {self.category}, date: {self.date}"

    




class Comments(models.Model):
    content = models.CharField(max_length = 300)
    auction = models.ForeignKey(listings, on_delete=models.CASCADE, related_name="listing")


    def __str__(self):
        return f"comment id: {self.pk},  content: {self.content}, auction comment was made on:{self.auction}"

    

class User(AbstractUser):
    balance = models.DecimalField(default=5000, max_digits =10, decimal_places=2)
    auctions = models.ManyToManyField(listings, blank = True, related_name="owner")
    comments = models.ManyToManyField(Comments, blank = True, related_name="user")

class Bids(models.Model):
    amount = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    auction = models.ForeignKey(listings, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="bids")



    def __str__(self):
        return f"id: {self.pk},bidding amount: {self.amount}, auction: {self.auction}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "watcher")
    listing = models.ForeignKey(listings, on_delete=models.CASCADE, related_name="watched_item")
    added = models.BooleanField(default = False)