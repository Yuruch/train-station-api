from django.db import transaction
from rest_framework import serializers

from train_station.models import (
    TrainType,
    Train,
    Station,
    Route,
    Crew,
    Journey,
    Ticket,
    Order,
)


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = ("id", "name")


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = (
            "id",
            "name",
            "cargo_num",
            "places_in_cargo",
            "train_type",
            "image",
        )
        read_only_fields = ("id", "image")


class TrainImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = ("id", "image")


class TrainListSerializer(TrainSerializer):
    train_type = serializers.CharField(source="train_type.name")


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ("id", "name", "latitude", "longitude")


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")

    def create(self, validated_data):
        source = validated_data.pop("source")
        destination = validated_data.pop("destination")
        route = Route.objects.create(
            source=source, destination=destination, **validated_data
        )
        return route


class RouteListSerializer(RouteSerializer):
    source = serializers.CharField(source="source.name")
    destination = serializers.CharField(source="destination.name")


class RouteDetailSerializer(RouteSerializer):
    source = StationSerializer()
    destination = StationSerializer()


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class JourneySerializer(serializers.ModelSerializer):

    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "departure_time",
            "arrival_time",
            "crew",
            "train",
        )

    def validate(self, data):
        if data.get("arrival_time") <= data.get("departure_time"):
            raise serializers.ValidationError(
                f"Arrival time must be later than departure time."
            )
        return data


class TicketTakenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["cargo", "seat"]


class JourneyListSerializer(JourneySerializer):
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    train = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    route = serializers.SerializerMethodField()
    tickets_available = serializers.IntegerField()

    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "departure_time",
            "arrival_time",
            "crew",
            "train",
            "tickets_available",
        )

    def get_route(self, obj):
        return str(obj.route)

    def get_tickets_available(self, obj):
        return obj.tickets_available


class JourneyDetailSerializer(JourneySerializer):
    crew = CrewSerializer(many=True)
    train = TrainSerializer(many=False)
    route = RouteListSerializer(many=False)
    tickets_available = serializers.IntegerField(read_only=True)
    taken_places = TicketTakenSerializer(
        source="tickets", many=True, read_only=True
    )

    class Meta:
        model = Journey
        fields = (
            "id",
            "route",
            "departure_time",
            "arrival_time",
            "crew",
            "train",
            "tickets_available",
            "taken_places",
        )


class TicketSummarySerializer(serializers.ModelSerializer):
    route = serializers.SerializerMethodField()
    train = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "route", "train")

    def get_route(self, obj):
        return str(obj.journey.route)

    def get_train(self, obj):
        return obj.journey.train.name


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ("id", "cargo", "seat", "journey")

    def validate(self, data):
        journey = data.get("journey")
        if journey:
            if not (1 <= data.get("seat") <= journey.train.places_in_cargo):
                raise serializers.ValidationError(
                    f"Seat must be between 1 and {journey.train.places_in_cargo}."
                )
            if not (1 <= data.get("cargo") <= journey.train.cargo_num):
                raise serializers.ValidationError(
                    f"Cargo must be between 1 and {journey.train.cargo_num}."
                )
        return data


class TicketDetailSerializer(TicketSerializer):
    journey = JourneyListSerializer(many=False)


class OrderListSerializer(serializers.ModelSerializer):
    tickets = TicketSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")


class OrderDetailSerializer(serializers.ModelSerializer):
    tickets = TicketDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")


class OrderCreateSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)

            return order
