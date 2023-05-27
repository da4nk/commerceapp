from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    image = models.URLField(default = "no image")
    price = models.DecimalField(default = 0, max_digits=10, decimal_places=2)
    category = models.CharField(default = "", max_length=20)

    def __str__(self):
        return f"id of the auction: {self.id}, name of the item: {self.title}, description of item: {self.description}, image of item: {self.image}, cost of item: {self.price}, category the item is in: {self.category}"

