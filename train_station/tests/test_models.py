from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from train_station.models import (
    TrainType,
    Train,
    Station,
    Route,
    Crew,
    Order,
    Ticket,
    Journey,
)
from user.models import CustomUser


class TrainTypeTestCase(TestCase):
    def test_str_method(self):
        train_type = TrainType.objects.create(name="Express")
        self.assertEqual(str(train_type), "Express")


class TrainTestCase(TestCase):
    def test_str_method(self):
        train_type = TrainType.objects.create(name="Freight")
        train = Train.objects.create(
            name="Train A",
            cargo_num=100,
            places_in_cargo=50,
            train_type=train_type,
        )
        self.assertEqual(str(train), "Train A (type: Freight)")


class StationTestCase(TestCase):
    def test_str_method(self):
        station = Station.objects.create(
            name="Central Station", latitude=51.50, longitude=-0.12
        )
        self.assertEqual(str(station), "Central Station")


class RouteTestCase(TestCase):
    def setUp(self):
        self.source = Station.objects.create(
            name="Source Station", latitude=51.50, longitude=-0.12
        )
        self.destination = Station.objects.create(
            name="Destination Station", latitude=48.85, longitude=2.35
        )

    def test_str_method(self):
        route = Route.objects.create(
            source=self.source, destination=self.destination, distance=200
        )
        self.assertEqual(str(route), "Source Station - Destination Station")

    def test_unique_together_constraint(self):
        Route.objects.create(
            source=self.source, destination=self.destination, distance=200
        )
        with self.assertRaises(ValidationError):
            route = Route(
                source=self.source, destination=self.destination, distance=150
            )
            route.full_clean()


class CrewTestCase(TestCase):
    def test_full_name_property(self):
        crew = Crew.objects.create(first_name="John", last_name="Doe")
        self.assertEqual(crew.full_name, "John Doe")

    def test_str_method(self):
        crew = Crew.objects.create(first_name="Jane", last_name="Doe")
        self.assertEqual(str(crew), "Jane Doe")


class OrderTestCase(TestCase):
    def test_order_creation(self):
        user = CustomUser.objects.create_user(
            email="testuser@example.com", password="password123"
        )  # Adjust as needed if not used
        order = Order.objects.create(user=user)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.user, user)


class TicketTestCase(TestCase):
    def setUp(self):
        self.train_type = TrainType.objects.create(name="Passenger")
        self.train = Train.objects.create(
            name="Train B",
            cargo_num=100,
            places_in_cargo=50,
            train_type=self.train_type,
        )
        self.station1 = Station.objects.create(
            name="Station A", latitude=51.50, longitude=-0.12
        )
        self.station2 = Station.objects.create(
            name="Station B", latitude=48.85, longitude=2.35
        )
        self.route = Route.objects.create(
            source=self.station1, destination=self.station2, distance=150
        )
        self.journey = Journey.objects.create(
            route=self.route,
            train=self.train,
            departure_time=timezone.now() + timezone.timedelta(hours=1),
            arrival_time=timezone.now() + timezone.timedelta(hours=3),
        )
        self.order = Order.objects.create(
            user=CustomUser.objects.create_user(
                email="testuser@example.com", password="password123"
            )
        )  # Adjust as needed if not used

    def test_clean_method(self):
        ticket = Ticket(
            cargo=50, seat=30, journey=self.journey, order=self.order
        )
        ticket.clean()  # Should pass without raising ValidationError

    def test_clean_method_invalid_seat(self):
        ticket = Ticket(
            cargo=50,
            seat=60,  # Invalid seat number
            journey=self.journey,
            order=self.order,
        )
        with self.assertRaises(ValidationError):
            ticket.clean()  # Should raise ValidationError for seat

    def test_clean_method_invalid_cargo(self):
        ticket = Ticket(
            cargo=150,  # Invalid cargo number
            seat=30,
            journey=self.journey,
            order=self.order,
        )
        with self.assertRaises(ValidationError):
            ticket.clean()  # Should raise ValidationError for cargo

    def test_str_method(self):
        ticket = Ticket.objects.create(
            cargo=10, seat=20, journey=self.journey, order=self.order
        )
        self.assertEqual(
            str(ticket), f"{self.journey} (train - 10, seat - 20)"
        )


class JourneyTestCase(TestCase):
    def setUp(self):
        self.source = Station.objects.create(
            name="Source", latitude=51.50, longitude=-0.12
        )
        self.destination = Station.objects.create(
            name="Destination", latitude=48.85, longitude=2.35
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=200
        )
        self.train = Train.objects.create(
            name="Train C",
            cargo_num=200,
            places_in_cargo=100,
            train_type=TrainType.objects.create(name="Local"),
        )
        self.crew = Crew.objects.create(first_name="Alice", last_name="Smith")

    def test_clean_method(self):
        journey = Journey(
            route=self.route,
            train=self.train,
            departure_time=timezone.now() + timezone.timedelta(hours=1),
            arrival_time=timezone.now() + timezone.timedelta(hours=3),
        )
        journey.clean()  # Should pass without raising ValidationError

    def test_clean_method_invalid_times(self):
        journey = Journey(
            route=self.route,
            train=self.train,
            departure_time=timezone.now() + timezone.timedelta(hours=3),
            arrival_time=timezone.now() + timezone.timedelta(hours=1),
        )
        with self.assertRaises(ValidationError):
            journey.clean()  # Should raise ValidationError for invalid times

    def test_str_method(self):
        journey = Journey.objects.create(
            route=self.route,
            train=self.train,
            departure_time=timezone.now() + timezone.timedelta(hours=1),
            arrival_time=timezone.now() + timezone.timedelta(hours=3),
        )
        self.assertEqual(
            str(journey),
            f"{self.route} ({journey.departure_time}"
            f" - {journey.arrival_time})",
        )
