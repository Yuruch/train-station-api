from django.test import TestCase

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
from train_station.serializers import (
    TrainTypeSerializer,
    TrainSerializer,
    StationSerializer,
    RouteSerializer,
    CrewSerializer,
    JourneySerializer,
    TicketSerializer,
    OrderCreateSerializer,
    OrderListSerializer,
)
from user.models import CustomUser


class TrainTypeSerializerTest(TestCase):
    def setUp(self):
        self.train_type = TrainType.objects.create(name="Freight")

    def test_train_type_serializer(self):
        serializer = TrainTypeSerializer(instance=self.train_type)
        data = serializer.data
        self.assertEqual(data["name"], "Freight")


class TrainSerializerTest(TestCase):
    def setUp(self):
        self.train_type = TrainType.objects.create(name="Freight")
        self.train = Train.objects.create(
            name="Train A",
            cargo_num=10,
            places_in_cargo=100,
            train_type=self.train_type,
        )

    def test_train_serializer(self):
        serializer = TrainSerializer(instance=self.train)
        data = serializer.data
        self.assertEqual(data["name"], "Train A")
        self.assertEqual(data["cargo_num"], 10)
        self.assertEqual(data["places_in_cargo"], 100)
        self.assertEqual(data["train_type"], self.train_type.id)


class StationSerializerTest(TestCase):
    def setUp(self):
        self.station = Station.objects.create(
            name="Station A", latitude=12.34, longitude=56.78
        )

    def test_station_serializer(self):
        serializer = StationSerializer(instance=self.station)
        data = serializer.data
        self.assertEqual(data["name"], "Station A")
        self.assertEqual(data["latitude"], "12.34")
        self.assertEqual(data["longitude"], "56.78")


class RouteSerializerTest(TestCase):
    def setUp(self):
        self.source = Station.objects.create(
            name="Source", latitude=12.34, longitude=56.78
        )
        self.destination = Station.objects.create(
            name="Destination", latitude=23.45, longitude=67.89
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=100
        )

    def test_route_serializer(self):
        serializer = RouteSerializer(instance=self.route)
        data = serializer.data
        self.assertEqual(data["source"], self.source.id)
        self.assertEqual(data["destination"], self.destination.id)
        self.assertEqual(data["distance"], 100)


class CrewSerializerTest(TestCase):
    def setUp(self):
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")

    def test_crew_serializer(self):
        serializer = CrewSerializer(instance=self.crew)
        data = serializer.data
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["last_name"], "Doe")


class JourneySerializerTest(TestCase):
    def setUp(self):
        self.source = Station.objects.create(
            name="Source", latitude=12.34, longitude=56.78
        )
        self.destination = Station.objects.create(
            name="Destination", latitude=23.45, longitude=67.89
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=100
        )
        self.train_type = TrainType.objects.create(name="Freight")
        self.train = Train.objects.create(
            name="Train A",
            cargo_num=10,
            places_in_cargo=100,
            train_type=self.train_type,
        )
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")
        self.journey = Journey.objects.create(
            route=self.route,
            train=self.train,
            departure_time="2024-08-15T08:00:00Z",
            arrival_time="2024-08-15T12:00:00Z",
        )
        self.journey.crew.add(self.crew)

    def test_journey_serializer(self):
        serializer = JourneySerializer(instance=self.journey)
        data = serializer.data
        self.assertEqual(data["route"], 1)
        self.assertEqual(data["train"], 1)
        self.assertEqual(data["departure_time"], "2024-08-15T08:00:00Z")
        self.assertEqual(data["arrival_time"], "2024-08-15T12:00:00Z")
        self.assertEqual(data["crew"][0], 1)


class TicketSerializerTest(TestCase):
    def setUp(self):
        self.source = Station.objects.create(
            name="Source", latitude=12.34, longitude=56.78
        )
        self.destination = Station.objects.create(
            name="Destination", latitude=23.45, longitude=67.89
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=100
        )
        self.train_type = TrainType.objects.create(name="Freight")
        self.train = Train.objects.create(
            name="Train A",
            cargo_num=10,
            places_in_cargo=100,
            train_type=self.train_type,
        )
        self.journey = Journey.objects.create(
            route=self.route,
            train=self.train,
            departure_time="2024-08-15T08:00:00Z",
            arrival_time="2024-08-15T12:00:00Z",
        )
        self.order = Order.objects.create(
            user=CustomUser.objects.create_user(
                email="testuser@example.com", password="password123"
            )
        )
        self.ticket = Ticket.objects.create(
            cargo=1, seat=1, journey=self.journey, order=self.order
        )

    def test_ticket_serializer(self):
        serializer = TicketSerializer(instance=self.ticket)
        data = serializer.data
        self.assertEqual(data["cargo"], 1)
        self.assertEqual(data["seat"], 1)
        self.assertEqual(data["journey"], self.journey.id)


class OrderSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="password123"
        )
        self.source = Station.objects.create(
            name="Source", latitude=12.34, longitude=56.78
        )
        self.destination = Station.objects.create(
            name="Destination", latitude=23.45, longitude=67.89
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=100
        )
        self.train_type = TrainType.objects.create(name="Freight")
        self.train = Train.objects.create(
            name="Train A",
            cargo_num=10,
            places_in_cargo=100,
            train_type=self.train_type,
        )
        self.journey = Journey.objects.create(
            route=self.route,
            train=self.train,
            departure_time="2024-08-15T08:00:00Z",
            arrival_time="2024-08-15T12:00:00Z",
        )
        self.order = Order.objects.create(user=self.user)

        self.ticket = Ticket.objects.create(
            cargo=1, seat=1, journey=self.journey, order=self.order
        )

    def test_order_serializer(self):
        serializer = OrderListSerializer(instance=self.order)
        data = serializer.data

        self.assertEqual(len(data["tickets"]), 1)
        self.assertEqual(data["tickets"][0]["cargo"], 1)
        self.assertEqual(data["tickets"][0]["seat"], 1)
        self.assertEqual(data["tickets"][0]["route"], str(self.route))
        self.assertEqual(data["tickets"][0]["train"], self.train.name)


class OrderCreateSerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="password123"
        )
        self.source = Station.objects.create(
            name="Source", latitude=12.34, longitude=56.78
        )
        self.destination = Station.objects.create(
            name="Destination", latitude=23.45, longitude=67.89
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=100
        )
        self.train_type = TrainType.objects.create(name="Freight")
        self.train = Train.objects.create(
            name="Train A",
            cargo_num=10,
            places_in_cargo=100,
            train_type=self.train_type,
        )
        self.journey = Journey.objects.create(
            route=self.route,
            train=self.train,
            departure_time="2024-08-15T08:00:00Z",
            arrival_time="2024-08-15T12:00:00Z",
        )
        self.ticket_data = {"cargo": 1, "seat": 1, "journey": self.journey.id}
        self.order_data = {"tickets": [self.ticket_data]}

    def test_order_create_serializer(self):
        serializer = OrderCreateSerializer(
            data=self.order_data, context={"request": None}
        )
        if serializer.is_valid():
            order = serializer.save(user=self.user)
            self.assertEqual(Order.objects.count(), 1)
            self.assertEqual(Ticket.objects.count(), 1)
            self.assertEqual(order.tickets.first().cargo, 1)
        else:
            self.fail(f"Serializer errors: {serializer.errors}")
