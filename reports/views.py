from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg
from accounts.decorators import farmer_required, buyer_required, admin_required
from marketplace.models import CropListing
from contracts.models import Contract
from deliveries.models import Delivery
from payments.models import Payment
from disputes.models import Dispute
from accounts.models import User

@farmer_required
def farmer_reports(request):
    user = request.user
    crops = CropListing.objects.filter(farmer=user)
    contracts = Contract.objects.filter(farmer=user)

    total_volume_listed = crops.aggregate(t=Sum("total_quantity_kg"))["t"] or 0
    total_volume_contracted = contracts.aggregate(t=Sum("quantity_kg"))["t"] or 0
    total_contract_value = contracts.aggregate(t=Sum("total_value"))["t"] or 0
    total_settled_earnings = Payment.objects.filter(recipient=user, status=Payment.Status.SUCCESS).aggregate(t=Sum("amount"))["t"] or 0
    pending_earnings = Payment.objects.filter(recipient=user, status=Payment.Status.PENDING).aggregate(t=Sum("amount"))["t"] or 0

    contract_status_stats = contracts.values("status").annotate(count=Count("id"))
    crop_stats = crops.values("crop_name").annotate(total_qty=Sum("total_quantity_kg"), active_qty=Sum("available_quantity_kg"))

    context = {
        "total_volume_listed": total_volume_listed,
        "total_volume_contracted": total_volume_contracted,
        "total_contract_value": total_contract_value,
        "total_settled_earnings": total_settled_earnings,
        "pending_earnings": pending_earnings,
        "contract_status_stats": contract_status_stats,
        "crop_stats": crop_stats,
    }
    return render(request, "reports/farmer_reports.html", context)


@buyer_required
def buyer_reports(request):
    user = request.user
    contracts = Contract.objects.filter(buyer=user)

    total_procurement_value = contracts.aggregate(t=Sum("total_value"))["t"] or 0
    total_kg_procured = contracts.aggregate(t=Sum("quantity_kg"))["t"] or 0
    total_paid = Payment.objects.filter(payer=user, status=Payment.Status.SUCCESS).aggregate(t=Sum("amount"))["t"] or 0
    total_pending_pay = Payment.objects.filter(payer=user, status=Payment.Status.PENDING).aggregate(t=Sum("amount"))["t"] or 0

    crop_breakdown = contracts.values("crop_name").annotate(
        qty=Sum("quantity_kg"),
        spend=Sum("total_value")
    )

    context = {
        "total_procurement_value": total_procurement_value,
        "total_kg_procured": total_kg_procured,
        "total_paid": total_paid,
        "total_pending_pay": total_pending_pay,
        "crop_breakdown": crop_breakdown,
    }
    return render(request, "reports/buyer_reports.html", context)


@admin_required
def admin_reports(request):
    total_users = User.objects.count()
    total_farmers = User.objects.filter(role=User.Role.FARMER).count()
    total_buyers = User.objects.filter(role=User.Role.BUYER).count()

    total_listings = CropListing.objects.count()
    total_contracts = Contract.objects.count()
    total_volume_inr = Contract.objects.aggregate(t=Sum("total_value"))["t"] or 0
    total_payments_cleared = Payment.objects.filter(status=Payment.Status.SUCCESS).aggregate(t=Sum("amount"))["t"] or 0

    dispute_count = Dispute.objects.count()
    dispute_resolved = Dispute.objects.filter(status=Dispute.Status.RESOLVED).count()

    context = {
        "total_users": total_users,
        "total_farmers": total_farmers,
        "total_buyers": total_buyers,
        "total_listings": total_listings,
        "total_contracts": total_contracts,
        "total_volume_inr": total_volume_inr,
        "total_payments_cleared": total_payments_cleared,
        "dispute_count": dispute_count,
        "dispute_resolved": dispute_resolved,
    }
    return render(request, "reports/admin_reports.html", context)
