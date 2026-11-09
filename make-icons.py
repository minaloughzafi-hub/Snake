# يولد كل الأيقونات من icon.png (يخدم داخل GitHub Actions)
from PIL import Image, ImageDraw, ImageChops
import os

src = Image.open('icon.png').convert('RGBA')
GREEN = (107, 209, 82)

r, g, b = src.convert('RGB').split()
mn = ImageChops.darker(ImageChops.darker(r, g), b)
alpha = mn.point(lambda v: max(0, min(255, int((v - 150) * 255 / 105))))
disc = Image.new('L', src.size, 0)
ImageDraw.Draw(disc).ellipse([30, 30, 270, 270], fill=255)
alpha = ImageChops.multiply(alpha, disc)

def sharp(a):
    return a.point(lambda v: max(0, min(255, int((v - 70) * 255 / 115))))

def snake_layer(size):
    L = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    L.putalpha(sharp(alpha.resize((size, size), Image.LANCZOS)))
    return L

def composite(size):
    bg = Image.new('RGBA', (size, size), GREEN + (255,))
    bg.alpha_composite(snake_layer(size))
    return bg

def round_icon(size):
    S = size * 4
    crop = src.crop((19, 19, 281, 281)).resize((S, S), Image.LANCZOS)
    m = Image.new('L', (S, S), 0)
    ImageDraw.Draw(m).ellipse([1, 1, S - 2, S - 2], fill=255)
    crop.putalpha(m)
    return crop.resize((size, size), Image.LANCZOS)

# أيقونات الويب
os.makedirs('www', exist_ok=True)
round_icon(192).save('www/icon-192.png')
round_icon(512).save('www/icon-512.png')
composite(512).convert('RGB').save('www/icon-maskable-512.png')

# موارد Android
base = 'resources/res'
legacy = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}
fore = {'mdpi': 108, 'hdpi': 162, 'xhdpi': 216, 'xxhdpi': 324, 'xxxhdpi': 432}
for d in legacy:
    os.makedirs(f'{base}/mipmap-{d}', exist_ok=True)
    composite(legacy[d]).convert('RGB').save(f'{base}/mipmap-{d}/ic_launcher.png')
    round_icon(legacy[d]).save(f'{base}/mipmap-{d}/ic_launcher_round.png')
    snake_layer(fore[d]).save(f'{base}/mipmap-{d}/ic_launcher_foreground.png')
os.makedirs(f'{base}/values', exist_ok=True)
with open(f'{base}/values/ic_launcher_background.xml', 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
            '    <color name="ic_launcher_background">#6BD152</color>\n</resources>\n')
Image.new('RGB', (16, 16), (172, 182, 7)).save('resources/splash-solid.png')
print('icons generated')
