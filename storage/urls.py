from django.urls import path
from storage import views

app_name = "items"

urlpatterns = [
    path("", views.index, name="index"),
]
