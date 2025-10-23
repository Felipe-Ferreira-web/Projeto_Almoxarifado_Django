from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Item(models.Model):

    item_id = models.BigAutoField(primary_key=True)
    object = models.CharField(max_length=20)
    description = models.CharField()
    quantity = models.IntegerField(default=1)
    storage_location = models.CharField()
    is_available = models.BooleanField()
    created_date = models.DateTimeField(default=timezone.now)
    owner_id = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.description}"
