from django.urls import path
from . import views

urlpatterns = [
    path("", views.marketplace_list, name="marketplace"),
    path("crop/<int:pk>/", views.crop_detail, name="crop_detail"),

    # Farmer portal routes
    path("farmer/dashboard/", views.farmer_dashboard, name="farmer_dashboard"),
    path("farmer/crops/", views.my_crops, name="my_crops"),
    path("farmer/crops/add/", views.crop_create, name="crop_create"),
    path("farmer/crops/<int:pk>/edit/", views.crop_update, name="crop_update"),
    path("farmer/crops/<int:pk>/toggle-status/", views.crop_status_toggle, name="crop_status_toggle"),

    # Aliases
    path("my-listings/", views.my_crops),
    path("add/", views.crop_create),
]
