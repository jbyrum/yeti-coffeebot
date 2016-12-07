import datetime
import django
from django.db import models
from django.utils import timezone
import math


class Temperature(models.Model):
    brew_date = models.DateTimeField(auto_now_add=True, blank=True)
    temperature = models.FloatField()

    def minutes_since_creation(self):
        time_delta = django.utils.timezone.now() - self.brew_date
        seconds = time_delta.total_seconds()
        minutes = math.ceil(seconds / 60)
        return minutes