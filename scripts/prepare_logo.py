import base64
from PIL import Image, ImageEnhance

# Load original generated image
img_path = r"d:\Code_Files\Projects\KALKI 1.5\kalki_symbol.jpg"
img = Image.open(img_path).convert("RGBA")

# Enhance brightness & contrast for extreme visibility at small icon sizes
enhancer = ImageEnhance.Contrast(img)
img_enhanced = enhancer.enhance(1.4)

brightener = ImageEnhance.Brightness(img_enhanced)
img_final = brightener.enhance(1.2)

# Save as PNG formats
png_path = r"d:\Code_Files\Projects\KALKI 1.5\kalki_symbol.png"
fav_png_path = r"d:\Code_Files\Projects\KALKI 1.5\favicon.png"
pub_png_path = r"d:\Code_Files\Projects\KALKI 1.5\frontend\public\kalki_symbol.png"
pub_fav_path = r"d:\Code_Files\Projects\KALKI 1.5\frontend\public\favicon.png"

img_final.save(png_path, "PNG")
img_final.save(fav_png_path, "PNG")
img_final.save(pub_png_path, "PNG")
img_final.save(pub_fav_path, "PNG")

# Convert small 64x64 favicon to base64 data string
fav_small = img_final.resize((64, 64), Image.Resampling.LANCZOS)
fav_small.save(r"d:\Code_Files\Projects\KALKI 1.5\favicon_64.png", "PNG")

with open(r"d:\Code_Files\Projects\KALKI 1.5\favicon_64.png", "rb") as f:
    b64_str = base64.b64encode(f.read()).decode("utf-8")
    data_uri = f"data:image/png;base64,{b64_str}"

with open(r"d:\Code_Files\Projects\KALKI 1.5\kalki_symbol_b64.txt", "w") as out_f:
    out_f.write(data_uri)

print("LOGO & FAVICON PROCESSED SUCCESSFULLY. BASE64 SAVED.")
