import os
import shutil
import django
from decimal import Decimal
from datetime import date, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings
from accounts.models import User
from farms.models import Farm
from marketplace.models import CropCategory, CropListing

media_crops_dir = os.path.join(settings.MEDIA_ROOT, "crops")
os.makedirs(media_crops_dir, exist_ok=True)

# 1. Categories
horticulture, _ = CropCategory.objects.get_or_create(
    name="Horticulture & Fruits",
    defaults={"description": "High value fresh orchard produce, GI-tagged fruits, and plantation crops.", "icon": "bi-apple"}
)
spices = CropCategory.objects.get(name="Vegetables & Spices")
pulses = CropCategory.objects.get(name="Pulses & Legumes")

# 2. Farmers & Farms
farmer1 = User.objects.get(username="farmer1")
farmer2 = User.objects.get(username="farmer2")

farm1 = Farm.objects.filter(farmer=farmer1).first()
farm2 = Farm.objects.filter(farmer=farmer2).first()

# Create additional specialty farm if needed
farm_south, _ = Farm.objects.get_or_create(
    farmer=farmer2,
    farm_name="Malabar & Konkan Plantation Estate",
    defaults={
        "survey_number": "PLOT-77/A",
        "village": "Wayanad Hills",
        "district": "Wayanad",
        "state": "Kerala",
        "area_acres": Decimal("25.0"),
        "soil_type": "Rich Red Laterite & Forest Loam",
        "irrigation_source": "Drip Micro-Sprinkler & Mountain Spring",
    }
)

new_crops_data = [
    {
        "farmer": farmer2,
        "farm": farm_south,
        "category": spices,
        "crop_name": "Guntur Teja Red Chilli",
        "variety": "S-17 Teja Export Grade",
        "total_qty": Decimal("4000.00"),
        "price": Decimal("210.00"),
        "grade": "Export Grade (Max 10% Moisture, High Heat)",
        "harvest_days": 15,
        "desc": "High capsaicin content (0.5%+) vibrant crimson red chillies sun-dried on clean tarpaulins. Rigorously tested for zero aflatoxin residue.",
        "src_image": r"C:\Users\anshi\.gemini\antigravity-ide\brain\ac1d0268-ff8b-44c2-a4ce-4e6ba699fd20\crop_red_chilli_1793525921990.jpg",
        "filename": "guntur_teja_red_chilli.jpg"
    },
    {
        "farmer": farmer2,
        "farm": farm_south,
        "category": horticulture,
        "crop_name": "Ratnagiri Alphonso Mangoes",
        "variety": "GI Tag Certified Hapus",
        "total_qty": Decimal("3500.00"),
        "price": Decimal("140.00"),
        "grade": "Grade A+ (Export Quality 250g+)",
        "harvest_days": 25,
        "desc": "Authentic GI-registered Devgad/Ratnagiri Hapus mangoes naturally tree-ripened without chemical calcium carbide. Rich saffron aroma and fiberless pulp.",
        "src_image": r"C:\Users\anshi\.gemini\antigravity-ide\brain\ac1d0268-ff8b-44c2-a4ce-4e6ba699fd20\crop_mangoes_1793525944772.jpg",
        "filename": "ratnagiri_alphonso_mangoes.jpg"
    },
    {
        "farmer": farmer1,
        "farm": farm1,
        "category": pulses,
        "crop_name": "Organic Desi Chickpeas (Chana)",
        "variety": "JG-11 Bold Gold Grain",
        "total_qty": Decimal("8000.00"),
        "price": Decimal("68.00"),
        "grade": "Machine Cleaned 99.5% Purity",
        "harvest_days": 30,
        "desc": "Non-GMO organic brown desi chickpeas grown in deep black cotton soils under integrated pest management. High protein 22%+, ideal for besan milling and packaging.",
        "src_image": r"C:\Users\anshi\.gemini\antigravity-ide\brain\ac1d0268-ff8b-44c2-a4ce-4e6ba699fd20\crop_chickpeas_1793525964957.jpg",
        "filename": "organic_desi_chickpeas.jpg"
    },
    {
        "farmer": farmer2,
        "farm": farm_south,
        "category": spices,
        "crop_name": "Malabar Tellicherry Black Pepper",
        "variety": "TGSEB Extra Bold (4.75mm+)",
        "total_qty": Decimal("1200.00"),
        "price": Decimal("620.00"),
        "grade": "Export Garbled Extra Bold",
        "harvest_days": 40,
        "desc": "World-famous Malabar black pepper hand-harvested from shaded hill slopes of Wayanad. High piperine, intense pungency, and natural sun-dried aroma.",
        "src_image": r"C:\Users\anshi\.gemini\antigravity-ide\brain\ac1d0268-ff8b-44c2-a4ce-4e6ba699fd20\crop_black_pepper_1793525981766.jpg",
        "filename": "malabar_black_pepper.jpg"
    },
    {
        "farmer": farmer1,
        "farm": farm1,
        "category": horticulture,
        "crop_name": "Shimla Royal Delicious Apples",
        "variety": "Grade A Royal Delicious",
        "total_qty": Decimal("5000.00"),
        "price": Decimal("115.00"),
        "grade": "Export Grade (75-85mm Caliber)",
        "harvest_days": 18,
        "desc": "Crisp, juicy mountain apples cultivated at 7,000 ft altitude in Shimla valley. Plucked at peak brix sugar level, sorted into standard corrugated trays.",
        "src_image": r"C:\Users\anshi\.gemini\antigravity-ide\brain\ac1d0268-ff8b-44c2-a4ce-4e6ba699fd20\crop_apples_1793526028449.jpg",
        "filename": "shimla_royal_delicious_apples.jpg"
    }
]

today = date.today()

for c_info in new_crops_data:
    dest_path = os.path.join(media_crops_dir, c_info["filename"])
    if os.path.exists(c_info["src_image"]):
        shutil.copyfile(c_info["src_image"], dest_path)
    
    crop, created = CropListing.objects.update_or_create(
        crop_name=c_info["crop_name"],
        defaults={
            "farmer": c_info["farmer"],
            "farm": c_info["farm"],
            "category": c_info["category"],
            "variety": c_info["variety"],
            "total_quantity_kg": c_info["total_qty"],
            "available_quantity_kg": c_info["total_qty"],
            "expected_price_per_kg": c_info["price"],
            "quality_grade": c_info["grade"],
            "expected_harvest_date": today + timedelta(days=c_info["harvest_days"]),
            "available_from": today + timedelta(days=c_info["harvest_days"] + 3),
            "description": c_info["desc"],
            "crop_image": f"crops/{c_info['filename']}",
            "status": CropListing.Status.ACTIVE
        }
    )
    status_str = "Created" if created else "Updated"
    print(f"{status_str}: {crop.crop_name} (Category: {crop.category.name}, Price: INR {crop.expected_price_per_kg}/kg)")

print(f"\nTotal Crop Listings in Platform: {CropListing.objects.count()}")
