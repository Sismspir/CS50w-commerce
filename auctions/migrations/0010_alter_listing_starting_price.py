# Generated by Django 4.1.7 on 2023-04-20 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_rename_price_listing_starting_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='starting_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
