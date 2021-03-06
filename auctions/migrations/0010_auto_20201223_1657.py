# Generated by Django 3.1.2 on 2020-12-23 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_remove_bid_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='bids_in_auction', to='auctions.Bid'),
        ),
        migrations.AddField(
            model_name='listing',
            name='last_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_bid', to='auctions.bid'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auction_for_bid', to='auctions.listing'),
        ),
    ]
