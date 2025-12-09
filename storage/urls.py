from django.urls import path
from storage import views
from django.conf.urls.static import static
from django.conf import settings

"""
URL configuration for the 'storage' application, namespaced as 'items'.

Defines the routing paths for all major application functionalities, 
including:
1. General views (index, search).
2. Item management (CRUD operations: create, detail, update, delete).
3. User authentication (register, login, logout, update, profile viewing).
4. Transaction handling (viewing history and processing loans/devolutions).

The urlpatterns list also includes configuration for serving media files in 
development environments.
"""

app_name = "items"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    # item (CRUD)
    path("items/<int:item_id>/detail/", views.item, name="item"),
    path("items/create/", views.create, name="create"),
    path("items/<int:item_id>/update/", views.update, name="update"),
    path("items/<int:item_id>/delete/", views.delete, name="delete"),
    # user (CRUD)
    path("user/register/", views.register, name="register"),
    path("user/login/", views.login_view, name="login"),
    path("user/logout/", views.logout_view, name="logout"),
    path("user/update/", views.user_update, name="user_update"),
    # user (view)
    path("user/profile/<int:user_id>/detail/", views.user_profile, name="user_profile"),
    # transactions
    path("transactions", views.Transactions, name="transactions"),
    path(
        "loan/<int:item_id>/",
        views.ItemTransaction,
        name="transaction",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
