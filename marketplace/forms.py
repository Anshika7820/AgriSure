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
<<<<<<< HEAD
            "farm": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "crop_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Sharbati Wheat, Basmati 1121"}),
            "variety": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. PBW-343"}),
            "total_quantity_kg": forms.NumberInput(attrs={"class": "form-control", "step": "any", "min": "0.01", "placeholder": "e.g. 5000", "id": "id_total_quantity_kg"}),
            "expected_price_per_kg": forms.NumberInput(attrs={"class": "form-control", "step": "any", "min": "0.01", "placeholder": "e.g. 26.50", "id": "id_expected_price_per_kg"}),
            "quality_grade": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Grade A (Standard), Organic Certified"}),
            "expected_harvest_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "available_from": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "crop_image": forms.FileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Pesticide threshold, moisture range, organic methods, packaging preferences..."}),
            "status": forms.Select(attrs={"class": "form-select"}),
=======
            "expected_harvest_date": forms.DateInput(attrs={"type": "date"}),
            "available_from": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
>>>>>>> origin/main
        }

    def __init__(self, *args, **kwargs):
        farmer = kwargs.pop("farmer", None)
        super().__init__(*args, **kwargs)
        if farmer:
<<<<<<< HEAD
            farmer_farms = Farm.objects.filter(farmer=farmer)
            self.fields["farm"].queryset = farmer_farms
            self.fields["farm"].empty_label = "Select one of your registered farms"
            # If farmer only has 1 farm, pre-select it
            if farmer_farms.count() == 1 and not self.initial.get("farm") and not (self.data and self.data.get("farm")):
                self.fields["farm"].initial = farmer_farms.first().id

        # Defaults for new listings
        if not self.instance.pk:
            self.fields["status"].initial = CropListing.Status.ACTIVE
            if not self.initial.get("quality_grade") and not (self.data and self.data.get("quality_grade")):
                self.fields["quality_grade"].initial = "Grade A (Standard)"

    def clean(self):
        cleaned_data = super().clean()
        harvest_date = cleaned_data.get("expected_harvest_date")
        avail_date = cleaned_data.get("available_from")
        if harvest_date and avail_date and avail_date < harvest_date:
            self.add_error("available_from", "Available dispatch date cannot be earlier than the expected harvest date.")
        qty = cleaned_data.get("total_quantity_kg")
        if qty is not None and qty <= 0:
            self.add_error("total_quantity_kg", "Total harvest yield must be greater than zero.")
        price = cleaned_data.get("expected_price_per_kg")
        if price is not None and price <= 0:
            self.add_error("expected_price_per_kg", "Asking price per kg must be greater than zero.")
        return cleaned_data


class CropFilterForm(forms.Form):
    q = forms.CharField(required=False, label="Search Crop or Variety", widget=forms.TextInput(attrs={"placeholder": "e.g. Wheat, Basmati, Cotton...", "class": "form-control"}))
    category = forms.ModelChoiceField(queryset=CropCategory.objects.all(), required=False, empty_label="All Categories", widget=forms.Select(attrs={"class": "form-select"}))
    state = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "e.g. Punjab, Maharashtra...", "class": "form-control"}))
    min_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder": "Min ₹/kg", "class": "form-control"}))
    max_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder": "Max ₹/kg", "class": "form-control"}))
    min_qty = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder": "Min kg", "class": "form-control"}))
=======
            self.fields["farm"].queryset = Farm.objects.filter(farmer=farmer)
            self.fields["farm"].empty_label = "Select one of your registered farms"


class CropFilterForm(forms.Form):
    q = forms.CharField(required=False, label="Search Crop or Variety", widget=forms.TextInput(attrs={"placeholder": "e.g. Wheat, Basmati, Cotton..."}))
    category = forms.ModelChoiceField(queryset=CropCategory.objects.all(), required=False, empty_label="All Categories")
    state = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "e.g. Punjab, Maharashtra..."}))
    min_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder": "Min ₹/kg"}))
    max_price = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder": "Max ₹/kg"}))
    min_qty = forms.DecimalField(required=False, min_value=0, widget=forms.NumberInput(attrs={"placeholder": "Min kg"}))
>>>>>>> origin/main
    sort_by = forms.ChoiceField(
        choices=[
            ("-created_at", "Newest Listed"),
            ("expected_price_per_kg", "Price: Low to High"),
            ("-expected_price_per_kg", "Price: High to Low"),
            ("expected_harvest_date", "Harvest Date: Earliest"),
            ("-available_quantity_kg", "Quantity: Highest"),
        ],
        required=False,
<<<<<<< HEAD
        initial="-created_at",
        widget=forms.Select(attrs={"class": "form-select"})
=======
        initial="-created_at"
>>>>>>> origin/main
    )
