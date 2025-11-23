from django.urls import path
from storage import views
from django.conf.urls.static import static
from django.conf import settings

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
    path("user/profile/", views.user_owner_profile, name="user_owner_profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
