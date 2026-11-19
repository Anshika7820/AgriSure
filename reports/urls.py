from django.urls import path
from . import views

urlpatterns = [
    path("farmer/", views.farmer_reports, name="farmer_reports"),
    path("buyer/", views.buyer_reports, name="buyer_reports"),
    path("admin-reports/", views.admin_reports, name="admin_reports"),
]
