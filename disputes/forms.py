from django import forms
from .models import Dispute

class DisputeForm(forms.ModelForm):
    class Meta:
        model = Dispute
        fields = ["reason", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Specify exact dates, discrepancies, vehicle numbers, or quality test results..."}),
        }


class DisputeResolveForm(forms.ModelForm):
    class Meta:
        model = Dispute
        fields = ["status", "resolution_notes"]
        widgets = {
            "resolution_notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Official mediator instructions, settlement terms, or arbitration ruling..."}),
        }
