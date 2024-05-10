# Generated by Django 3.2.21 on 2024-05-09 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_auctionlisting_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(choices=[('no_category_listed', 'No Category Listed'), ('electronics', 'Electronics'), ('fashion', 'Fashion'), ('home', 'Home')], default='No_Category_Listed', max_length=50),
        ),
    ]
