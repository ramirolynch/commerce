# Generated by Django 3.1.2 on 2020-12-24 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auto_20201224_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='latestbid',
        ),
    ]