from django.db import models
from django.utils import timezone

# Create your models here.


class Item(models.Model):
    item_id = models.BigAutoField(primary_key=True)
    description = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    storage_location = models.CharField(blank=True)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    #  owner_id = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.description}"
