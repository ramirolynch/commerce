from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime  
from django.forms import ModelForm
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator



class User(AbstractUser):
    pass


class Listing(models.Model):
    seller = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    listing_name = models.CharField(max_length=64, null=True, blank=True)
    start_price = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True, verbose_name='Is active', null=True)
    url = models.TextField(null=True, blank=True, default="https://www.example.com")
    created = models.DateTimeField(auto_now_add=True)
    latestbid = models.ForeignKey('Bid', on_delete=models.CASCADE, related_name='latest_bid', blank=True, null=True)
    allbids = models.ManyToManyField('Bid', related_name='all_bids_for_auction', blank=True)

    CLEAN = 'Clean'
    BLUE = 'Blue'
    ABSURD = 'Absurd'
    DARK = 'Dark'
    POLITICAL = 'Political'

    COMEDY_GENRES = [
        (CLEAN, 'Clean'),
        (BLUE, 'Blue'),
        (DARK, 'Dark'),
        (ABSURD, 'Absurd'),
        (POLITICAL, 'Political'),
    ]
    
    comedy_category = models.CharField(
        max_length=44,
        choices=COMEDY_GENRES,
        default=CLEAN,
    )

    def __str__(self):
        return self.listing_name
 

class Bid(models.Model):
    bidder = models.ForeignKey('User', on_delete=models.CASCADE, related_name="buyer", null=True, blank=True)
    bid = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='auction_for_bid', null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s' % (self.bid)


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='commenter', null=True)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, null=True, related_name='relatedlisting')
    body = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return f'Comment by { self.user } on { self.timestamp }'


class Watchlist(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="watcher", null=True, blank=True)
    watch = models.ManyToManyField(Listing)

    def __str__(self):
        return 'Watchlist for %s' % (self.user)


# superuser user: rami pass: rami2020 email: rami@example.com
# user: amir email: amir@example.com pass: amir2020
