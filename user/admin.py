from django.contrib import admin

from user.models import CustomUser


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass
