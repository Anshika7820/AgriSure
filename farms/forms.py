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
<<<<<<< HEAD
        widgets = {
            "farm_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Green Valley Plot A"}),
            "village": forms.TextInput(attrs={"class": "form-control", "placeholder": "Village name"}),
            "district": forms.TextInput(attrs={"class": "form-control", "placeholder": "District"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "PIN code"}),
            "area_acres": forms.NumberInput(attrs={"class": "form-control", "step": "any", "min": "0.01", "placeholder": "e.g. 10.0"}),
            "soil_type": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Black Cotton, Sandy Loam"}),
            "irrigation_source": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Solar Tube Well, Canal"}),
            "survey_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Official revenue department number"}),
        }

    def clean_area_acres(self):
        area = self.cleaned_data.get("area_acres")
        if area is not None and area <= 0:
            raise forms.ValidationError("Farm area must be greater than zero acres.")
        return area
=======
>>>>>>> origin/main
