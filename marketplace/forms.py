from django import forms
from .models import CropListing, CropCategory
from farms.models import Farm

class CropListingForm(forms.ModelForm):
    class Meta:
        model = CropListing
        fields = [
            "farm",
            "category",
            "crop_name",
            "variety",
            "total_quantity_kg",
            "expected_price_per_kg",
            "quality_grade",
            "expected_harvest_date",
            "available_from",
            "crop_image",
            "description",
            "status",
        ]
        widgets = {
            "expected_harvest_date": forms.DateInput(attrs={"type": "date"}),
            "available_from": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        farmer = kwargs.pop("farmer", None)
        super().__init__(*args, **kwargs)
        if farmer:
            self.fields["farm"].queryset = Farm.objects.filter(farmer=farmer)
            self.fields["farm"].empty_label = "Select one of your registered farms"


class CropFilterForm(forms.Form):
    q = forms.CharField(required=False, label="Search Crop or Variety", widget=forms.TextInput(attrs={"placeholder": "e.g. Wheat, Basmati, Cotton..."}))
    category = forms.ModelChoiceField(queryset=CropCategory.objects.all(), required=False, empty_label="All Categories")
    state = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "e.g. Punjab, Maharashtra..."}))
    min_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder": "Min ₹/kg"}))
    max_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder": "Max ₹/kg"}))
    min_qty = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder": "Min kg"}))
    sort_by = forms.ChoiceField(
        choices=[
            ("-created_at", "Newest Listed"),
            ("expected_price_per_kg", "Price: Low to High"),
            ("-expected_price_per_kg", "Price: High to Low"),
            ("expected_harvest_date", "Harvest Date: Earliest"),
            ("-available_quantity_kg", "Quantity: Highest"),
        ],
        required=False,
        initial="-created_at"
    )
