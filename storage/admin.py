from django.contrib import admin

from storage import models

# Register your models here.


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "item_id",
        "object",
        "is_available",
        "created_date",
    )
    ordering = ("-item_id",)
    search_fields = ("item_id", "object")
    list_per_page = 20
