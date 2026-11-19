from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import User, FarmerProfile, BuyerProfile, VerificationDocument
from .forms import (
    FarmerRegistrationForm,
    BuyerRegistrationForm,
    FarmerProfileForm,
    BuyerProfileForm,
    VerificationDocumentForm,
)
from audit.models import AuditLog
from marketplace.models import CropListing
from contracts.models import Contract

def home(request):
    """Landing page showcasing AgriSure value proposition, live stats, and marketplace preview."""
    active_listings_count = CropListing.objects.filter(status=CropListing.Status.ACTIVE).count()
    active_contracts_count = Contract.objects.filter(status__in=[Contract.Status.ACTIVE, Contract.Status.COMPLETED]).count()
    total_farmers = User.objects.filter(role=User.Role.FARMER).count()
    total_buyers = User.objects.filter(role=User.Role.BUYER).count()

    featured_crops = CropListing.objects.filter(status=CropListing.Status.ACTIVE).select_related("farmer", "category")[:6]

    context = {
        "active_listings_count": active_listings_count,
        "active_contracts_count": active_contracts_count,
        "total_farmers": total_farmers,
        "total_buyers": total_buyers,
        "featured_crops": featured_crops,
    }
    return render(request, "home.html", context)


def register_farmer(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password"])
                user.role = User.Role.FARMER
                user.first_name = form.cleaned_data["first_name"]
                user.save()

                FarmerProfile.objects.create(
                    user=user,
                    village=form.cleaned_data["village"],
                    district=form.cleaned_data["district"],
                    state=form.cleaned_data["state"],
                    farm_area_acres=form.cleaned_data["farm_area_acres"],
                    farming_experience=form.cleaned_data["farming_experience"],
                    farm_name=f"{user.first_name}'s Farm"
                )

<<<<<<< HEAD
                # Provision primary farm location for seamless crop listing
                from farms.models import Farm
                Farm.objects.create(
                    farmer=user,
                    farm_name=f"{user.first_name}'s Farm",
                    village=form.cleaned_data["village"],
                    district=form.cleaned_data["district"],
                    state=form.cleaned_data["state"],
                    area_acres=form.cleaned_data["farm_area_acres"],
                )

=======
>>>>>>> origin/main
                AuditLog.log("USER_REGISTERED", "User", user.id, f"Farmer account registered for {user.username}", user=user)

                login(request, user)
                messages.success(request, f"Welcome to AgriSure, {user.first_name}! Your farmer account has been created.")
                return redirect("farmer_dashboard")
    else:
        form = FarmerRegistrationForm()

    return render(request, "accounts/register_farmer.html", {"form": form})


def register_buyer(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data["password"])
                user.role = User.Role.BUYER
                user.first_name = form.cleaned_data["first_name"]
                user.save()

                BuyerProfile.objects.create(
                    user=user,
                    business_name=form.cleaned_data["business_name"],
                    business_type=form.cleaned_data["business_type"],
                    address=form.cleaned_data["address"],
                    district=form.cleaned_data["district"],
                    state=form.cleaned_data["state"],
                    registration_number=form.cleaned_data["registration_number"]
                )

                AuditLog.log("USER_REGISTERED", "User", user.id, f"Buyer account registered for {user.username}", user=user)

                login(request, user)
                messages.success(request, f"Welcome to AgriSure, {form.cleaned_data['business_name']}! Your buyer account has been created.")
                return redirect("buyer_dashboard")
    else:
        form = BuyerRegistrationForm()

    return render(request, "accounts/register_buyer.html", {"form": form})


@login_required
def dashboard(request):
    """Directs logged in users to their role-specific dashboard."""
    if request.user.is_platform_admin() or request.user.is_superuser:
        return redirect("admin_dashboard")
    elif request.user.is_farmer():
        return redirect("farmer_dashboard")
    elif request.user.is_buyer():
        return redirect("buyer_dashboard")
    return render(request, "accounts/invalid_role.html")


@login_required
def profile_view(request):
    user = request.user
    docs = user.verification_documents.all()
    context = {"profile_user": user, "documents": docs}
    return render(request, "accounts/profile.html", context)


@login_required
def edit_profile(request):
    user = request.user
    if user.is_farmer():
        profile, _ = FarmerProfile.objects.get_or_create(user=user)
        if request.method == "POST":
            form = FarmerProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                user.first_name = request.POST.get("first_name", user.first_name)
                user.phone = request.POST.get("phone", user.phone)
                user.save()
                messages.success(request, "Your farmer profile details have been updated.")
                return redirect("profile")
        else:
            form = FarmerProfileForm(instance=profile)
    else:
        profile, _ = BuyerProfile.objects.get_or_create(user=user)
        if request.method == "POST":
            form = BuyerProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                user.first_name = request.POST.get("first_name", user.first_name)
                user.phone = request.POST.get("phone", user.phone)
                user.save()
                messages.success(request, "Your business profile details have been updated.")
                return redirect("profile")
        else:
            form = BuyerProfileForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {"form": form})


@login_required
def upload_verification(request):
    if request.method == "POST":
        form = VerificationDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.status = VerificationDocument.Status.PENDING
            doc.save()
            AuditLog.log("VERIFICATION_SUBMITTED", "VerificationDocument", doc.id, f"{doc.document_type} submitted for verification", user=request.user)
            messages.success(request, "Verification document submitted successfully for admin review.")
            return redirect("profile")
    else:
        form = VerificationDocumentForm()
    return render(request, "accounts/upload_verification.html", {"form": form})


def custom_logout(request):
<<<<<<< HEAD
    logout(request)
    messages.info(request, "You have been securely signed out.")
    return redirect("home")
=======
    if request.method == "POST":
        logout(request)
        messages.info(request, "You have been securely signed out.")
        return redirect("home")
    return redirect("dashboard")
>>>>>>> origin/main
