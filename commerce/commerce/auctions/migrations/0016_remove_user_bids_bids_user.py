# Generated by Django 4.1.7 on 2023-06-22 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_alter_user_bids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bids',
        ),
        migrations.AddField(
            model_name='bids',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bids', to=settings.AUTH_USER_MODEL),
        ),
    ]
