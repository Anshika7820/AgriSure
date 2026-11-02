from django import forms
from .models import Delivery

class DeliveryScheduleForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = [
            "scheduled_date",
            "quantity_scheduled_kg",
            "delivery_notes",
        ]
        widgets = {
            "scheduled_date": forms.DateInput(attrs={"type": "date"}),
            "delivery_notes": forms.Textarea(attrs={"rows": 2}),
        }


class DeliveryDispatchForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = [
            "quantity_delivered_kg",
            "delivery_notes",
        ]
        widgets = {
            "delivery_notes": forms.Textarea(attrs={"rows": 2, "placeholder": "Driver contact, vehicle registration number, dispatch slip #..."}),
        }


class DeliveryConfirmForm(forms.Form):
    DECISION_CHOICES = [
        ("CONFIRM", "Accept & Confirm Weighment"),
        ("REJECT", "Reject Batch / Major Quality Issue"),
    ]
    decision = forms.ChoiceField(choices=DECISION_CHOICES, widget=forms.RadioSelect)
    quantity_received_kg = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=False,
        label="Actual Net Weighbridge Weight (kg)"
    )
    rejection_reason = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2, "placeholder": "If rejecting or noting deduction, state quality testing metrics..."}),
        required=False
    )
