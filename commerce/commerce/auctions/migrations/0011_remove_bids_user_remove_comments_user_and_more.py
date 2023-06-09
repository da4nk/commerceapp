# Generated by Django 4.1.7 on 2023-06-03 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_remove_user_auctions_owned_remove_user_bids_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bids',
            name='user',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='user',
        ),
        migrations.RemoveField(
            model_name='listings',
            name='owner',
        ),
        migrations.AddField(
            model_name='user',
            name='auctions',
            field=models.ManyToManyField(blank=True, related_name='owner', to='auctions.listings'),
        ),
        migrations.AddField(
            model_name='user',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='owner', to='auctions.bids'),
        ),
        migrations.AddField(
            model_name='user',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='user', to='auctions.comments'),
        ),
    ]
