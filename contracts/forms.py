from django import forms
from .models import ContractAmendment

class ContractAmendmentForm(forms.ModelForm):
    class Meta:
        model = ContractAmendment
        fields = [
            "description",
            "adjusted_quantity_kg",
            "adjusted_price_per_kg",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "Explain the operational or climatic reason for proposing this amendment..."}),
        }


class ContractSignForm(forms.Form):
    digital_consent = forms.BooleanField(
        required=True,
        label="I certify that I have read and agree to all terms of this Agricultural Contract, and agree to electronic execution."
    )
