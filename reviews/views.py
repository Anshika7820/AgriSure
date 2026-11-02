from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Review
from .forms import ReviewForm
from contracts.models import Contract
from accounts.models import User
from audit.models import AuditLog

@login_required
def review_create(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)

    if request.user != contract.farmer and request.user != contract.buyer:
        messages.error(request, "Only contracting parties can leave a review.")
        return redirect("dashboard")

    if contract.status != Contract.Status.COMPLETED:
        messages.warning(request, "Reviews can only be submitted once the contract is fully completed.")
        return redirect("contract_detail", contract_id=contract.id)

    # Check if user already reviewed
    existing = Review.objects.filter(contract=contract, reviewer=request.user).first()
    if existing:
        messages.info(request, "You have already submitted your review for this contract.")
        return redirect("contract_detail", contract_id=contract.id)

    reviewed_user = contract.buyer if request.user == contract.farmer else contract.farmer

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.contract = contract
            rev.reviewer = request.user
            rev.reviewed_party = reviewed_user
            rev.save()

            AuditLog.log("REVIEW_SUBMITTED", "Review", rev.id, f"{request.user.username} rated {reviewed_user.username} {rev.rating}/5", user=request.user)
            messages.success(request, f"Thank you! Your {rev.rating}-star review for {reviewed_user.get_full_name() or reviewed_user.username} has been posted.")
            return redirect("contract_detail", contract_id=contract.id)
    else:
        form = ReviewForm()

    return render(request, "reviews/create.html", {"form": form, "contract": contract, "reviewed_user": reviewed_user})


def reviews_for_user(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    reviews = Review.objects.filter(reviewed_party=target_user).select_related("reviewer", "contract")
    return render(request, "reviews/user_reviews.html", {"target_user": target_user, "reviews": reviews})
