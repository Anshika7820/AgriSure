from django.urls import path
from . import views

urlpatterns = [
    # Buyer portal
    path("buyer/dashboard/", views.buyer_dashboard, name="buyer_dashboard"),
    path("buyer/offers/", views.buyer_offers_list, name="buyer_offers"),
    path("offers/create/<int:crop_id>/", views.offer_create, name="offer_create"),

    # Farmer portal
    path("farmer/offers/", views.farmer_offers_list, name="farmer_offers"),

    # Common negotiation endpoints
    path("offers/<int:offer_id>/", views.offer_detail, name="offer_detail"),
    path("offers/<int:offer_id>/counter/", views.offer_counter, name="offer_counter"),
    path("offers/<int:offer_id>/accept/", views.offer_accept, name="offer_accept"),
    path("offers/<int:offer_id>/reject/", views.offer_reject, name="offer_reject"),
    path("offers/<int:offer_id>/withdraw/", views.offer_withdraw, name="offer_withdraw"),

    # Real-time message API
    path("api/offers/<int:offer_id>/messages/", views.api_offer_messages, name="api_offer_messages"),

    # Aliases
    path("offers/", views.farmer_offers_list),
    path("my-offers/", views.buyer_offers_list),
]
