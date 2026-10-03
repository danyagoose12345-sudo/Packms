import os
from PIL import Image

source_dir = "icons_files"
target_dir = "ico_files"

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Переименование старого файла, если необходимо
old_png = os.path.join(source_dir, "rtmp-edit.png")
new_png = os.path.join(source_dir, "rtmp-text.png")
if os.path.exists(old_png) and not os.path.exists(new_png):
    os.rename(old_png, new_png)

icon_files = ["rtmp-text.png", "we-can.png", "of-tka.png", "source.png", "of-main.png"]

print("Конвертация картинок в формат .ico...")
for file_name in icon_files:
    source_path = os.path.join(source_dir, file_name)
    if os.path.exists(source_path):
        img = Image.open(source_path)
        ico_name = file_name.replace(".png", ".ico")
        ico_path = os.path.join(target_dir, ico_name)
        img.save(ico_path, format="ICO", sizes=[(32, 32), (48, 48), (64, 64), (128, 128)])
        print(f"Успешно создана иконка: {ico_path}")
