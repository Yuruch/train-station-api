# Generated by Django 5.1 on 2024-08-08 07:12

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("train_station", "0004_alter_journey_departure_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="journey",
            name="departure_time",
            field=models.DateTimeField(
                validators=[
                    django.core.validators.MinValueValidator(
                        datetime.datetime(2024, 8, 8, 7, 12, 18, 7728)
                    )
                ]
            ),
        ),
    ]
