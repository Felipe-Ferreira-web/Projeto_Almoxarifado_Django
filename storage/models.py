from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Item(models.Model):
    item_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    storage_location = models.CharField(blank=True)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    owner_id = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.description}"
