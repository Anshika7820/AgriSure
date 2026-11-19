from django.urls import path
from . import views

urlpatterns = [
    path("", views.farm_list, name="farm_list"),
    path("add/", views.farm_create, name="farm_create"),
    path("<int:pk>/", views.farm_detail, name="farm_detail"),
    path("<int:pk>/edit/", views.farm_update, name="farm_update"),
]
