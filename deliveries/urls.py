from django.urls import path
from . import views

urlpatterns = [
    path("", views.delivery_list, name="delivery_list"),
    path("<int:delivery_id>/", views.delivery_detail, name="delivery_detail"),
    path("<int:delivery_id>/dispatch/", views.delivery_dispatch, name="delivery_dispatch"),
    path("<int:delivery_id>/confirm/", views.delivery_confirm, name="delivery_confirm"),
]
