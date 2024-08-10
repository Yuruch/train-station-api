from django.db.models import Count, F
from rest_framework import viewsets, permissions

from train_station.models import TrainType, Train, Station, Route, Crew, Journey, Order
from train_station.serializers import (
    TrainTypeSerializer,
    TrainSerializer,
    TrainListSerializer,
    StationSerializer,
    RouteSerializer,
    RouteListSerializer,
    CrewSerializer,
    JourneySerializer,
    JourneyListSerializer,
    JourneyDetailSerializer,
    RouteDetailSerializer,
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
)


class TrainTypeViewSet(viewsets.ModelViewSet):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer
    search_fields = ["name"]
    ordering_fields = ["name"]


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    search_fields = ["name", "train_type__name"]
    ordering_fields = ["name", "train_type__name"]

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            return queryset.select_related("train_type")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer
        else:
            return TrainSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    search_fields = ["name"]
    ordering_fields = ["name"]


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    ordering_fields = ["source__name", "destination__name", "distance"]

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list" or self.action == "retrieve":
            return queryset.select_related("source", "destination")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action == "retrieve":
            return RouteDetailSerializer
        else:
            return RouteSerializer

    search_fields = ["source__name", "destination__name"]


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["first_name", "last_name"]


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    search_fields = [""]
    ordering_fields = [
        "departure_time",
        "arrival_time",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        elif self.action == "retrieve":
            return JourneyDetailSerializer
        else:
            return JourneySerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action in ["list", "retrieve"]:
            queryset = (
                queryset.select_related(
                    "route__source", "route__destination", "train__train_type"
                )
                .prefetch_related("crew")
                .annotate(
                    tickets_available=F("train__cargo_num")
                    * F("train__places_in_cargo")
                    - Count("tickets")
                )
            )

        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        if self.action in ["list", "retrieve"]:
            return queryset.prefetch_related(
                "tickets__journey__route__source",
                "tickets__journey__route__destination",
                "tickets__journey__train",
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        elif self.action == "retrieve":
            return OrderDetailSerializer
        else:
            return OrderCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
