from django.urls import path
from storage import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "items"

urlpatterns = [
    path("<int:item_id>/", views.item, name="item"),
    path("search/", views.search, name="search"),
    path("", views.index, name="index"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
