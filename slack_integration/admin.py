from django.contrib import admin

# Register your models here.
from slack_integration.models import Temperature


class TemperatureAdmin(admin.ModelAdmin):
    list_display = ('brew_date', )


admin.site.register(Temperature, TemperatureAdmin)
