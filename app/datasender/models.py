from django.db import models
from django.utils.timezone import now


class Stamp(models.Model):
    object_cid = models.CharField(max_length=255, unique=True)
    time_tolerance = models.IntegerField(help_text="Time tolerance in minutes")
    created_date = models.DateTimeField(default=now, help_text="created_date datetime")

    def __str__(self):
        return f"Stamp for {self.object_cid}"
