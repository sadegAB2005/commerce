# Generated by Django 3.2.21 on 2024-05-09 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting_bid_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auction_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]