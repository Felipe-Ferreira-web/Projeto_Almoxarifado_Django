from django.contrib import admin

from storage import models

# Register your models here.


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Item model.

    Defines how the Item model appears and behaves in the Django administration site.
    It specifies which fields are displayed in the list view, how records are ordered,
    which fields are searchable, and the pagination limit.

    Attributes:
    -----------
    list_display : tuple
        Fields to display in the change list view of the admin interface.
    ordering : tuple
        Default ordering for the list view (descending by item_id).
    search_fields : tuple
        Fields that the admin search bar will query.
    list_per_page : int
        Maximum number of records to display per page in the change list view.
    """

    list_display = (
        "item_id",
        "object",
        "is_available",
        "created_date",
    )
    ordering = ("-item_id",)
    search_fields = ("item_id", "object")
    list_per_page = 20
