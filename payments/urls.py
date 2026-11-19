from django.urls import path
from . import views

urlpatterns = [
    path("", views.payment_list, name="payment_list"),
    path("<int:payment_id>/", views.payment_detail, name="payment_detail"),
    path("<int:payment_id>/checkout/", views.payment_checkout, name="payment_checkout"),
    path("<int:payment_id>/receipt/", views.payment_receipt_download, name="payment_receipt_download"),
]
