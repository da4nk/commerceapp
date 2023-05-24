from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class listings(models.Model):
    Title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    image = models.URLField()
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    def __str__(self):
        return f"{self.id}, {self.title}, {self.description}, {self.image}, {self.start_price}, {self.start_date}, {self.end_date}"

