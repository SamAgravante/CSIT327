# Generated by Django 5.1.3 on 2024-12-11 23:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_forums_isedited'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricehistory',
            name='itemName',
        ),
        migrations.AddField(
            model_name='pricehistory',
            name='watchlist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='price_histories', to='tracker.watchlist'),
        ),
    ]
