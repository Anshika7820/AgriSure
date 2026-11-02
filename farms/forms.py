from django import forms
from .models import Farm

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = [
            "farm_name",
            "village",
            "district",
            "state",
            "postal_code",
            "area_acres",
            "soil_type",
            "irrigation_source",
            "survey_number",
        ]
