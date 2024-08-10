from rest_framework import viewsets, status, permissions, generics, filters

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


class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.all()
    search_fields = ["name", "train_type__name"]

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer
        else:
            return TrainSerializer


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    search_fields = ["name"]


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()

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


class JourneyViewSet(viewsets.ModelViewSet):
    queryset = Journey.objects.all()
    search_fields = [""]

    def get_serializer_class(self):
        if self.action == "list":
            return JourneyListSerializer
        elif self.action == "retrieve":
            return JourneyDetailSerializer
        else:
            return JourneySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        elif self.action == "retrieve":
            return OrderDetailSerializer
        else:
            return OrderCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
