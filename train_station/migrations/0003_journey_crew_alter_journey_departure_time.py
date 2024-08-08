# Generated by Django 5.1 on 2024-08-08 06:49

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("train_station", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="journey",
            name="crew",
            field=models.ManyToManyField(
                related_name="journeys", to="train_station.crew"
            ),
        ),
        migrations.AlterField(
            model_name="journey",
            name="departure_time",
            field=models.DateTimeField(
                validators=[
                    django.core.validators.MinValueValidator(
                        datetime.datetime(2024, 8, 8, 6, 49, 30, 824887)
                    )
                ]
            ),
        ),
    ]