from django.contrib import admin

from train_station.models import (
    Journey,
    Ticket,
    Order,
    Crew,
    Route,
    Station,
    Train,
    TrainType,
)


# Register your models here.
@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    pass


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    pass


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    pass


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    pass


@admin.register(TrainType)
class TrainTypeAdmin(admin.ModelAdmin):
    pass
