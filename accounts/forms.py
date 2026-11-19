from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import User, FarmerProfile, BuyerProfile, VerificationDocument

class FarmerRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label="Full Name")
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True, label="Mobile Number")
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    village = forms.CharField(max_length=100, required=True)
    district = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    farm_area_acres = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label="Total Land Area (Acres)")
    farming_experience = forms.IntegerField(min_value=0, required=True, label="Experience (Years)")
    agree_terms = forms.BooleanField(required=True, label="I agree to AgriSure Contract Farming Terms & Code of Conduct")

    class Meta:
        model = User
        fields = ["username", "email", "phone"]

    def clean_confirm_password(self):
        p1 = self.cleaned_data.get("password")
        p2 = self.cleaned_data.get("confirm_password")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        validate_password(p1)
        return p2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email


class BuyerRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label="Authorized Contact Name")
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True, label="Business Phone Number")
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    business_name = forms.CharField(max_length=200, required=True, label="Company / Entity Name")
    business_type = forms.ChoiceField(choices=BuyerProfile.BusinessType.choices, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), required=True, label="Registered Business Address")
    district = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    registration_number = forms.CharField(max_length=100, required=True, label="GST / Corporate ID / FSSAI No.")
    agree_terms = forms.BooleanField(required=True, label="I agree to AgriSure Procurement & Contract Terms")

    class Meta:
        model = User
        fields = ["username", "email", "phone"]

    def clean_confirm_password(self):
        p1 = self.cleaned_data.get("password")
        p2 = self.cleaned_data.get("confirm_password")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        validate_password(p1)
        return p2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email


class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ["farm_name", "village", "district", "state", "postal_code", "farm_area_acres", "farming_experience", "primary_crops", "bio", "avatar"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
        }


class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ["business_name", "business_type", "contact_person", "address", "district", "state", "postal_code", "registration_number", "avatar"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }


class VerificationDocumentForm(forms.ModelForm):
    class Meta:
        model = VerificationDocument
        fields = ["document_type", "document_file"]
