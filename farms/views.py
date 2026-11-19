from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.decorators import farmer_required
from .models import Farm
from .forms import FarmForm
from audit.models import AuditLog

@farmer_required
def farm_list(request):
    farms = Farm.objects.filter(farmer=request.user)
    return render(request, "farmer/farms/list.html", {"farms": farms})


@farmer_required
def farm_create(request):
    if request.method == "POST":
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.farmer = request.user
            farm.save()
            AuditLog.log("FARM_CREATED", "Farm", farm.id, f"Added farm '{farm.farm_name}' ({farm.area_acres} acres)", user=request.user)
            messages.success(request, f"Farm '{farm.farm_name}' successfully added to your profile.")
<<<<<<< HEAD
            if not request.user.crop_listings.exists():
                return redirect("crop_create")
            return redirect("farm_list")
        else:
            messages.error(request, "Could not add farm plot. Please review the errors below.")
=======
            return redirect("farm_list")
>>>>>>> origin/main
    else:
        form = FarmForm()
    return render(request, "farmer/farms/form.html", {"form": form, "action": "Add New Farm"})


@farmer_required
def farm_update(request, pk):
    farm = get_object_or_404(Farm, pk=pk, farmer=request.user)
    if request.method == "POST":
        form = FarmForm(request.POST, instance=farm)
        if form.is_valid():
            form.save()
            AuditLog.log("FARM_UPDATED", "Farm", farm.id, f"Updated farm '{farm.farm_name}'", user=request.user)
            messages.success(request, f"Farm '{farm.farm_name}' details updated successfully.")
            return redirect("farm_list")
    else:
        form = FarmForm(instance=farm)
    return render(request, "farmer/farms/form.html", {"form": form, "action": f"Edit {farm.farm_name}", "farm": farm})


@farmer_required
def farm_detail(request, pk):
    farm = get_object_or_404(Farm, pk=pk, farmer=request.user)
    listings = farm.crop_listings.all()
    return render(request, "farmer/farms/detail.html", {"farm": farm, "listings": listings})
