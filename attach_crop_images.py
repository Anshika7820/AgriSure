import os
import shutil
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings
from marketplace.models import CropListing

target_dir = os.path.join(settings.MEDIA_ROOT, "crops")
os.makedirs(target_dir, exist_ok=True)

images_map = {
    "Sharbati Premium Wheat": r"C:\Users\anshi\.gemini\antigravity-ide\brain\ac1d0268-ff8b-44c2-a4ce-4e6ba699fd20\crop_wheat_1793524221233.jpg",
    "Traditional Basmati Rice 1121": r"C:\Users\anshi\.gemini\antigravity-ide\brain\ac1d0268-ff8b-44c2-a4ce-4e6ba699fd20\crop_rice_1793524242037.jpg",
    "Organic Bt Cotton (Long Staple)": r"C:\Users\anshi\.gemini\antigravity-ide\brain\ac1d0268-ff8b-44c2-a4ce-4e6ba699fd20\crop_cotton_1793524258835.jpg",
    "Yellow Mustard (Pusa Bold)": r"C:\Users\anshi\.gemini\antigravity-ide\brain\ac1d0268-ff8b-44c2-a4ce-4e6ba699fd20\crop_mustard_1793524279907.jpg",
    "Salem Turmeric Fingers": r"C:\Users\anshi\.gemini\antigravity-ide\brain\ac1d0268-ff8b-44c2-a4ce-4e6ba699fd20\crop_turmeric_1793524300235.jpg",
}

for crop_name, src_path in images_map.items():
    if os.path.exists(src_path):
        filename = f"{crop_name.lower().replace(' ', '_')}.jpg"
        dest_path = os.path.join(target_dir, filename)
        shutil.copyfile(src_path, dest_path)
        
        crops = CropListing.objects.filter(crop_name=crop_name)
        for c in crops:
            c.crop_image = f"crops/{filename}"
            c.save(update_fields=["crop_image"])
            print(f"Updated {c.crop_name} with image crops/{filename}")
    else:
        print(f"File not found: {src_path}")

print("All crop images attached successfully.")
