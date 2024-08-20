from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from train_station.models import (
    TrainType,
    Train,
    Station,
    Route,
    Crew,
    Journey,
    Order,
    Ticket,
)
from user.models import CustomUser

User = get_user_model()


class TrainTypeViewSetTests(APITestCase):
    def setUp(self):
        self.train_type = TrainType.objects.create(name="Freight")
        self.url = reverse("train_station:traintype-list")

    def test_list_train_types(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_create_train_type(self):
        data = {"name": "Passenger"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TrainType.objects.count(), 2)


class TrainViewSetTests(APITestCase):
    def setUp(self):
        self.train_type = TrainType.objects.create(name="Freight")
        self.train = Train.objects.create(
            name="Train1",
            cargo_num=10,
            places_in_cargo=100,
            train_type=self.train_type,
        )
        self.url = reverse("train_station:train-list")

    def test_list_trains(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_create_train(self):
        data = {
            "name": "Train2",
            "cargo_num": 5,
            "places_in_cargo": 80,
            "train_type": self.train_type.id,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Train.objects.count(), 2)


class StationViewSetTests(APITestCase):
    def setUp(self):
        self.station = Station.objects.create(
            name="Central Station", latitude=50.45, longitude=30.52
        )
        self.url = reverse("train_station:station-list")

    def test_list_stations(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_create_station(self):
        data = {"name": "North Station", "latitude": 50.5, "longitude": 30.6}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Station.objects.count(), 2)


class RouteViewSetTests(APITestCase):
    def setUp(self):
        self.station1 = Station.objects.create(
            name="Station A", latitude=50.45, longitude=30.52
        )
        self.station2 = Station.objects.create(
            name="Station B", latitude=50.46, longitude=30.53
        )
        self.route = Route.objects.create(
            source=self.station1, destination=self.station2, distance=100
        )
        self.url = reverse("train_station:route-list")

    def test_list_routes(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_create_route(self):
        station3 = Station.objects.create(
            name="Station C", latitude=22.45, longitude=10.52
        )
        station4 = Station.objects.create(
            name="Station D", latitude=22.46, longitude=10.53
        )
        data = {
            "source": station3.id,
            "destination": station4.id,
            "distance": 150,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Route.objects.count(), 2)


class JourneyViewSetTests(APITestCase):
    def setUp(self):
        self.station1 = Station.objects.create(
            name="Station A", latitude=50.45, longitude=30.52
        )
        self.station2 = Station.objects.create(
            name="Station B", latitude=50.46, longitude=30.53
        )
        self.route = Route.objects.create(
            source=self.station1, destination=self.station2, distance=100
        )
        self.train_type = TrainType.objects.create(name="Passenger")
        self.train = Train.objects.create(
            name="Train1",
            cargo_num=5,
            places_in_cargo=50,
            train_type=self.train_type,
        )
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")
        self.journey = Journey.objects.create(
            route=self.route,
            train=self.train,
            departure_time=timezone.now() + timedelta(hours=1),
            arrival_time=timezone.now() + timedelta(hours=2),
        )
        self.journey.crew.add(self.crew)
        self.url = reverse("train_station:journey-list")

    def test_list_journeys(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(response.data["count"]), 1)

    def test_create_journey(self):
        data = {
            "route": self.route.id,
            "train": self.train.id,
            "departure_time": timezone.now() + timedelta(hours=3),
            "arrival_time": timezone.now() + timedelta(hours=5),
            "crew": [self.crew.id],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Journey.objects.count(), 2)


class OrderViewSetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.train_type = TrainType.objects.create(name="Express")
        self.train = Train.objects.create(
            name="Express 1",
            cargo_num=10,
            places_in_cargo=100,
            train_type=self.train_type,
        )
        self.station1 = Station.objects.create(
            name="Station A", latitude=50.45, longitude=30.52
        )
        self.station2 = Station.objects.create(
            name="Station B", latitude=50.46, longitude=30.53
        )
        self.route = Route.objects.create(
            source=self.station1, destination=self.station2, distance=100
        )
        self.journey = Journey.objects.create(
            route=self.route,
            train=self.train,
            departure_time=timezone.now() + timezone.timedelta(days=1),
            arrival_time=timezone.now() + timezone.timedelta(days=1, hours=2),
        )

        self.url = reverse("train_station:order-list")

    def test_list_orders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_create_order_with_tickets(self):
        order_data = {
            "tickets": [
                {"cargo": 1, "seat": 10, "journey": self.journey.id},
                {"cargo": 2, "seat": 20, "journey": self.journey.id},
            ],
        }

        response = self.client.post(self.url, order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 2)
        order = Order.objects.last()
        self.assertEqual(order.tickets.count(), 2)

    def test_order_permissions(self):
        other_user = User.objects.create_user(
            email="other@example.com", password="password123"
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
