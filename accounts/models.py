from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        FARMER = "FARMER", "Farmer"
        BUYER = "BUYER", "Buyer"
        ADMIN = "ADMIN", "Administrator"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.FARMER
    )
    phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_farmer(self):
        return self.role == self.Role.FARMER

    def is_buyer(self):
        return self.role == self.Role.BUYER

    def is_platform_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class FarmerProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="farmer_profile"
    )
    farm_name = models.CharField(max_length=150, blank=True)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=12, blank=True)
    farm_area_acres = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0
    )
    farming_experience = models.PositiveIntegerField(default=0, help_text="Years of farming experience")
    primary_crops = models.CharField(max_length=200, blank=True, help_text="Comma-separated crops")
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.farm_name or f"{self.user.get_full_name() or self.user.username}'s Farm"


class BuyerProfile(models.Model):
    class BusinessType(models.TextChoices):
        WHOLESALER = "WHOLESALER", "Wholesaler / Grain Trader"
        FOOD_PROCESSOR = "FOOD_PROCESSOR", "Food Processing Company"
        EXPORTER = "EXPORTER", "Agri-Export House"
        RETAILER = "RETAILER", "Retail Chain / Supermarket"
        OTHER = "OTHER", "Institutional Buyer / Other"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="buyer_profile"
    )
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(
        max_length=50,
        choices=BusinessType.choices,
        default=BusinessType.WHOLESALER
    )
    contact_person = models.CharField(max_length=100, blank=True)
    address = models.TextField()
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=12, blank=True)
    registration_number = models.CharField(
        max_length=100,
        blank=True,
        help_text="GST / Corporate ID / FSSAI number"
    )
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name or self.user.username


class VerificationDocument(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending Review"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="verification_documents"
    )
    document_type = models.CharField(
        max_length=50,
        help_text="e.g. Aadhaar Card, Land Record / Khasra-Khatauni, GST Certificate, FSSAI License"
    )
    document_file = models.FileField(upload_to="documents/")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    admin_notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.document_type} ({self.get_status_display()})"
