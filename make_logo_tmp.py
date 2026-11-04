"""ساخت لوگوی دایره‌ای همسو از پوستر (یک‌بار مصرف)."""
from PIL import Image, ImageDraw

SRC = r"C:\Users\darkoob.org\AppData\Roaming\Qoder\SharedClientCache\cache\images\873946c0\IMG_20261014_174958_531-5c5492c3.jpg"
OUT = r"f:\project\Hamsoo\core\static\core\img\logo.png"

src = Image.open(SRC).convert('RGB')
w, h = src.size
print('source size:', w, h)

# ساخت لوگوی دایره‌ای: کل پوستر (مربع) با ماسک دایره‌ای — واترمارک «همسو» کامل در مرکز
D = 1024
poster = src.resize((D, D), Image.LANCZOS)

mask = Image.new('L', (D, D), 0)
ImageDraw.Draw(mask).ellipse((0, 0, D, D), fill=255)
out = Image.new('RGBA', (D, D))
out.paste(poster, (0, 0), mask)
out.save(OUT)
print('saved:', OUT, out.size)
