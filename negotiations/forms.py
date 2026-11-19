from django import forms
from .models import Offer, NegotiationMessage

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            "quantity_kg",
            "proposed_price_per_kg",
            "delivery_date",
            "delivery_location",
            "quality_specifications",
            "message",
        ]
        widgets = {
            "delivery_date": forms.DateInput(attrs={"type": "date"}),
            "quality_specifications": forms.Textarea(attrs={"rows": 2, "placeholder": "Moisture limit, cleaning standards, packaging requirements..."}),
            "message": forms.Textarea(attrs={"rows": 3, "placeholder": "Introduce your procurement requirements to the farmer..."}),
        }


class CounterOfferForm(forms.ModelForm):
    class Meta:
        model = NegotiationMessage
        fields = [
            "counter_price_per_kg",
            "counter_quantity_kg",
            "counter_delivery_date",
            "message",
        ]
        widgets = {
            "counter_delivery_date": forms.DateInput(attrs={"type": "date"}),
            "message": forms.Textarea(attrs={"rows": 2, "placeholder": "Explain reason for revised terms (e.g., market rate adjustment, transport cost)..."}),
        }
