# Generated by Django 4.1.7 on 2023-07-14 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_watchlist_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='closed_auction',
        ),
    ]
