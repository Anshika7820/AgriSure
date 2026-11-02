from django.urls import path
from . import views

urlpatterns = [
    path("", views.contract_list, name="contract_list"),
    path("<int:contract_id>/", views.contract_detail, name="contract_detail"),
    path("<int:contract_id>/sign/", views.contract_sign, name="contract_sign"),
    path("<int:contract_id>/amend/", views.contract_amend, name="contract_amend"),
    path("<int:contract_id>/amend/<int:amendment_id>/respond/", views.contract_amend_respond, name="contract_amend_respond"),
    path("<int:contract_id>/pdf/", views.contract_download_pdf, name="contract_download_pdf"),
]
