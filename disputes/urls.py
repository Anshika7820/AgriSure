from django.urls import path
from . import views

urlpatterns = [
    path("", views.dispute_list, name="dispute_list"),
    path("create/<int:contract_id>/", views.dispute_create, name="dispute_create"),
    path("<int:dispute_id>/", views.dispute_detail, name="dispute_detail"),
    path("<int:dispute_id>/resolve/", views.dispute_resolve, name="dispute_resolve"),
]
