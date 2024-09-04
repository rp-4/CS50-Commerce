from django.contrib.auth.models import AbstractUser
from django.db import models

from datetime import datetime as dt
from django.core.exceptions import ValidationError


class Users(AbstractUser):
    pass
    # id = models.CharField(max_length=100, primary_key=True)
    # username = models.CharField(max_length=40, unique=True)
    # password = models.CharField(max_length=100)
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    # email = models.CharField(max_length=100, unique=True)
    # is_active = models.CharField(max_length=100)
    # last_login = models.CharField(max_length=100)
    # date_joined = models.CharField(max_length=100)

class Categories(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=32, unique=True, null=False)

    def __str__(self):
        return f"{self.category}"


class Listings(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('deleted', 'Deleted'),
    ]

    id = models.IntegerField(primary_key=True)
    category_id = models.ForeignKey(Categories, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=225, unique=True, null=False)
    description = models.TextField(null=False)
    listing_price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    datetime_added = models.DateTimeField(default= dt.now, editable=False) #or use auto_now_add=True for default dt
    added_by_user_id = models.ForeignKey(Users, null=False, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default= 'active')

    def clean(self):
        super().clean()
        if self.listing_price <= 0:
            raise ValidationError('Listing price must be greater than zero.')

    def __str__(self):
        return f"{self.id}/n{self.category_id}/n{self.title}/n{self.listing_price}/n{self.added_by_user_id}"


class Images(models.Model):
    listing_id = models.ForeignKey(Listings, null=False, on_delete=models.CASCADE)
    image = models.FileField(unique=True, null=False)


class Comments(models.Model):
    user_id = models.ForeignKey(Users, null=False, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listings, null=False, on_delete=models.CASCADE)
    comment= models.TextField(null=False)
    timestamp = models.DateTimeField(default= dt.now, editable=False)


class Bids(models.Model):
    ACTION_CHOICES = [
        ('added', 'Added'),
        ('bid_placed', 'Bid_placed'),
    ]

    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(Users, null=False, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listings, null=False, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, default= 'added')
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    timestamp = models.DateTimeField(default= dt.now, editable=False)
    

class Winners(models.Model):
    listing_id = models.ForeignKey(Listings, null=False, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Users, null=False, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default= dt.now, editable=False)
    

class Watchlists(models.Model):
    user_id = models.ForeignKey(Users, null=False, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listings, null=False, on_delete=models.CASCADE)
