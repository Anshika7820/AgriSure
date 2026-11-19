from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from accounts.decorators import farmer_required
from .models import CropListing, CropCategory
from .forms import CropListingForm, CropFilterForm
from farms.models import Farm
from negotiations.models import Offer
from contracts.models import Contract
from deliveries.models import Delivery
from payments.models import Payment
from audit.models import AuditLog

def marketplace_list(request):
    """Public and buyer marketplace catalog with multi-faceted search and filtering."""
    queryset = CropListing.objects.filter(status=CropListing.Status.ACTIVE).select_related("farmer", "farm", "category")
    form = CropFilterForm(request.GET)

    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            queryset = queryset.filter(
                Q(crop_name__icontains=q) |
                Q(variety__icontains=q) |
                Q(description__icontains=q) |
                Q(farm__district__icontains=q)
            )

        category = form.cleaned_data.get("category")
        if category:
            queryset = queryset.filter(category=category)

        state = form.cleaned_data.get("state")
        if state:
            queryset = queryset.filter(farm__state__icontains=state)

        min_price = form.cleaned_data.get("min_price")
        if min_price:
            queryset = queryset.filter(expected_price_per_kg__gte=min_price)

        max_price = form.cleaned_data.get("max_price")
        if max_price:
            queryset = queryset.filter(expected_price_per_kg__lte=max_price)

        min_qty = form.cleaned_data.get("min_qty")
        if min_qty:
            queryset = queryset.filter(available_quantity_kg__gte=min_qty)

        sort_by = form.cleaned_data.get("sort_by") or "-created_at"
        queryset = queryset.order_by(sort_by)
    else:
        queryset = queryset.order_by("-created_at")

    paginator = Paginator(queryset, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = CropCategory.objects.all()

    context = {
        "page_obj": page_obj,
        "form": form,
        "categories": categories,
        "total_results": queryset.count(),
    }
    return render(request, "marketplace/list.html", context)


def crop_detail(request, pk):
    """Detailed view of a crop listing including farmer credentials and offer submission CTA."""
    crop = get_object_or_404(
        CropListing.objects.select_related("farmer", "farmer__farmer_profile", "farm", "category"),
        pk=pk
    )
    user_offer = None
    if request.user.is_authenticated and request.user.is_buyer():
        user_offer = Offer.objects.filter(crop_listing=crop, buyer=request.user).first()

    context = {
        "crop": crop,
        "user_offer": user_offer,
    }
    return render(request, "marketplace/detail.html", context)


@farmer_required
def farmer_dashboard(request):
    """Farmer Command Center with real-time analytics and quick actions."""
    user = request.user
    my_listings = CropListing.objects.filter(farmer=user)
    active_listings_count = my_listings.filter(status=CropListing.Status.ACTIVE).count()

    offers_received = Offer.objects.filter(crop_listing__farmer=user)
    pending_offers_count = offers_received.filter(status=Offer.Status.PENDING).count()

    contracts = Contract.objects.filter(farmer=user)
    active_contracts_count = contracts.filter(status=Contract.Status.ACTIVE).count()
    completed_contracts_count = contracts.filter(status=Contract.Status.COMPLETED).count()

    upcoming_deliveries = Delivery.objects.filter(
        contract__farmer=user,
        status__in=[Delivery.Status.SCHEDULED, Delivery.Status.READY_FOR_DISPATCH, Delivery.Status.IN_TRANSIT]
    ).count()

    # Financial calculations
    total_earnings = Payment.objects.filter(
        recipient=user,
        status=Payment.Status.SUCCESS
    ).aggregate(total=Sum("amount"))["total"] or 0

    pending_payments = Payment.objects.filter(
        recipient=user,
        status=Payment.Status.PENDING
    ).aggregate(total=Sum("amount"))["total"] or 0

    recent_offers = offers_received.select_related("buyer", "crop_listing")[:5]
    recent_contracts = contracts.select_related("buyer")[:5]

    context = {
        "active_listings_count": active_listings_count,
        "total_listings_count": my_listings.count(),
        "pending_offers_count": pending_offers_count,
        "active_contracts_count": active_contracts_count,
        "completed_contracts_count": completed_contracts_count,
        "upcoming_deliveries": upcoming_deliveries,
        "total_earnings": total_earnings,
        "pending_payments": pending_payments,
        "recent_offers": recent_offers,
        "recent_contracts": recent_contracts,
    }
    return render(request, "farmer/dashboard.html", context)


@farmer_required
def my_crops(request):
    """List of all crop listings created by the logged in farmer."""
    crops = CropListing.objects.filter(farmer=request.user).select_related("farm", "category").annotate(
        offer_count=Count("offers")
    )
    return render(request, "farmer/crops/list.html", {"crops": crops})


@farmer_required
def crop_create(request):
    """Farmer creates a new crop listing."""
    # Ensure farmer has at least one registered farm
    if not Farm.objects.filter(farmer=request.user).exists():
        # Auto-provision primary farm from profile if profile exists
        profile = getattr(request.user, "farmer_profile", None)
        if profile and (profile.village or profile.district or profile.farm_name):
            Farm.objects.create(
                farmer=request.user,
                farm_name=profile.farm_name or f"{request.user.get_full_name() or request.user.username}'s Farm",
                village=profile.village or "Primary Village",
                district=profile.district or "District",
                state=profile.state or "State",
                area_acres=profile.farm_area_acres or 5.0
            )
        else:
            messages.warning(request, "Please register at least one farm location before listing crops.")
            return redirect("farm_create")

    if request.method == "POST":
        form = CropListingForm(request.POST, request.FILES, farmer=request.user)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.farmer = request.user
            # Available quantity initially equals total quantity
            crop.available_quantity_kg = crop.total_quantity_kg
            crop.save()
            AuditLog.log("CROP_LISTED", "CropListing", crop.id, f"Listed crop '{crop.crop_name}' ({crop.total_quantity_kg}kg at ₹{crop.expected_price_per_kg}/kg)", user=request.user)
            messages.success(request, f"Crop '{crop.crop_name}' has been successfully published to the marketplace.")
            return redirect("my_crops")
        else:
            messages.error(request, "Could not add crop. Please review the highlighted errors below.")
    else:
        form = CropListingForm(farmer=request.user)

    return render(request, "farmer/crops/form.html", {"form": form, "action": "Add New Crop Listing"})


@farmer_required
def crop_update(request, pk):
    """Farmer updates an existing crop listing."""
    crop = get_object_or_404(CropListing, pk=pk, farmer=request.user)
    old_total = crop.total_quantity_kg
    old_avail = crop.available_quantity_kg
    if request.method == "POST":
        form = CropListingForm(request.POST, request.FILES, instance=crop, farmer=request.user)
        if form.is_valid():
            updated_crop = form.save(commit=False)
            # If no stock was reserved yet (available equaled total), sync available with new total
            if old_avail == old_total:
                updated_crop.available_quantity_kg = updated_crop.total_quantity_kg
            elif updated_crop.available_quantity_kg > updated_crop.total_quantity_kg:
                updated_crop.available_quantity_kg = updated_crop.total_quantity_kg
            updated_crop.save()
            AuditLog.log("CROP_UPDATED", "CropListing", crop.id, f"Updated crop '{crop.crop_name}'", user=request.user)
            messages.success(request, f"Listing for '{crop.crop_name}' updated successfully.")
            return redirect("my_crops")
        else:
            messages.error(request, "Could not update crop. Please review the highlighted errors below.")
    else:
        form = CropListingForm(instance=crop, farmer=request.user)

    return render(request, "farmer/crops/form.html", {"form": form, "action": f"Edit {crop.crop_name}", "crop": crop})


@farmer_required
def crop_status_toggle(request, pk):
    """Quickly activate, pause, or close a crop listing."""
    crop = get_object_or_404(CropListing, pk=pk, farmer=request.user)
    new_status = request.POST.get("status")
    if new_status in [s[0] for s in CropListing.Status.choices]:
        crop.status = new_status
        crop.save(update_fields=["status"])
        messages.info(request, f"Status of '{crop.crop_name}' updated to {crop.get_status_display()}.")
    return redirect("my_crops")
