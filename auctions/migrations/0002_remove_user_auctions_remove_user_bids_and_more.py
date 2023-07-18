# Generated by Django 4.1.7 on 2023-06-02 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='auctions',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bids',
        ),
        migrations.RemoveField(
            model_name='user',
            name='comments',
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
            field=models.ManyToManyField(blank=True, related_name='commenter', to='auctions.comments'),
        ),
    ]