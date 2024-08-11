# Generated by Django 5.1 on 2024-08-10 09:30

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("train_station", "0007_alter_journey_departure_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="journey",
            name="departure_time",
            field=models.DateTimeField(
                validators=[
                    django.core.validators.MinValueValidator(
                        datetime.datetime(
                            2024, 8, 10, 9, 30, 38, 224969, tzinfo=datetime.timezone.utc
                        )
                    )
                ]
            ),
        ),
    ]