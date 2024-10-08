import os
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class TrainType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


def train_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    name = instance.name[:50]
    filename = f"{slugify(name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/trains/", filename)


class Train(models.Model):
    name = models.CharField(max_length=255)
    cargo_num = models.IntegerField()
    places_in_cargo = models.IntegerField()
    train_type = models.ForeignKey(
        TrainType, on_delete=models.CASCADE, related_name="trains"
    )
    image = models.ImageField(null=True, upload_to=train_image_file_path)

    def __str__(self):
        return f"{self.name} (type: {self.train_type})"


class Station(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="routes_as_source"
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="routes_as_destination",
    )
    distance = models.IntegerField()

    class Meta:
        unique_together = (("source", "destination"),)

    def __str__(self):
        return f"{self.source.name} - {self.destination.name}"


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )


class Ticket(models.Model):
    cargo = models.IntegerField()
    seat = models.IntegerField()
    journey = models.ForeignKey(
        "Journey", on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        unique_together = (("cargo", "journey", "seat"),)

    def clean(self):
        super().clean()
        if not (1 <= self.seat <= self.journey.train.places_in_cargo):
            raise ValidationError(
                f"Seat must be between 1 and "
                f"{self.journey.train.places_in_cargo}."
            )
        if not (1 <= self.cargo <= self.journey.train.cargo_num):
            raise ValidationError(
                f"Cargo must be between 1 and {self.journey.train.cargo_num}."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.journey} (train - {self.cargo}, seat - {self.seat})"


class Journey(models.Model):
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="journeys"
    )
    train = models.ForeignKey(
        Train, on_delete=models.CASCADE, related_name="journeys"
    )
    departure_time = models.DateTimeField(
        validators=[MinValueValidator(timezone.now())],
    )
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="journeys")

    def clean(self):
        super().clean()
        if self.arrival_time <= self.departure_time:
            raise ValidationError(
                "Arrival time must be later than departure time."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.route} ({self.departure_time} - {self.arrival_time})"
