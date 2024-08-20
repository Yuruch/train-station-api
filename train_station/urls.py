from django.urls import path, include
from rest_framework import routers

from train_station.views import (
    TrainTypeViewSet,
    TrainViewSet,
    StationViewSet,
    RouteViewSet,
    CrewViewSet,
    JourneyViewSet,
    OrderViewSet,
)

app_name = "train_station"

router = routers.DefaultRouter()
router.register("train-types", TrainTypeViewSet)
router.register("trains", TrainViewSet)
router.register("stations", StationViewSet)
router.register("routes", RouteViewSet)
router.register("crews", CrewViewSet)
router.register("journeys", JourneyViewSet)
router.register("orders", OrderViewSet)


urlpatterns = [path("", include(router.urls))]
