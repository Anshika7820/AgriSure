from django.urls import path
from . import views

urlpatterns = [
    path("contract/<int:contract_id>/create/", views.review_create, name="review_create"),
    path("user/<int:user_id>/", views.reviews_for_user, name="user_reviews"),
]
