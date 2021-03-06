# Generated by Django 3.1.2 on 2020-12-28 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_listing_latestbid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='latestbid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='latest_bid', to='auctions.bid'),
        ),
    ]
