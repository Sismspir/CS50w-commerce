# Generated by Django 4.1.7 on 2023-04-16 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bid',
        ),
        migrations.AddField(
            model_name='listing',
            name='img',
            field=models.URLField(blank=True, null=True),
        ),
    ]