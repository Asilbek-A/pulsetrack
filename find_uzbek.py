#!/usr/bin/env python3
"""Find remaining Uzbek text in dart files."""
import os

# Common Uzbek words that appear in UI strings
uzbek_words = [
    'Boshlash', 'Tugatish', 'Davom', 'Tahrirlash', 'Saqlash', 'Bekor',
    'Maqsad', 'Hisobim', 'Bildirishnoma', 'Maxfiylik', 'Yordam', 'Haqida',
    'Bugun', 'Kecha', 'hafta', 'oy', 'yil',
    'Qayd', 'Reja', 'Jamiyat', 'Liderlar',
    'Marshru', 'Joylashuv',
    'Ulanmoqda', 'Ulangan', 'Ulanmagan',
    'Sinxron', 'Yangilash', 'Yuklanmoqda',
    'Qurilmani', 'qurilmangizni',
    'Hech narsa', 'hech narsa',
    'Tabriklaymiz', 'Yuborish',
    "ma'lumot", "ma'lumotlar",
    'oshmoqda', 'kamaymoqda',
    'Kalibr', 'kalibr',
    'bosqich', 'bosqichi',
    'Tiklnish', 'tiklnish',
    "Zo'riqish", "zo'riqish",
    "Ko'rsatkich", "ko'rsatkich",
    "Qo'shish", "qo'shish",
    "O'chirish", "o'chirish",
    "ko'rish", "Ko'rish",
    "ko'rsatish", "Ko'rsatish",
    'Kundalik', 'kundalik',
    'Sog\'liq', 'sog\'liq',
    'uyqu', 'Uyqu',
    'yurak', 'Yurak',
    'nafas', 'Nafas',
    'Qadam', 'qadam',
    'Masofa', 'masofa',
    'Tezlik', 'tezlik',
    'kaloriya', 'Kaloriya',
    'Batareya', 'batareya',
    'Signal', 'signal',
    'Versiya', 'versiya',
    'Izoh', 'izoh',
    'Yoqtirish', 'yoqtirish',
    'Statistika', 'statistika',
]

dart_dir = r"C:\Users\User\Desktop\whoop\whoop_app\lib"
found = {}

for root, dirs, files in os.walk(dart_dir):
    for fname in files:
        if fname.endswith('.dart'):
            path = os.path.join(root, fname)
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith('//') or stripped.startswith('import') or stripped.startswith('*'):
                    continue
                for word in uzbek_words:
                    if word in line and ("'" in line or '"' in line):
                        rel = path.replace(dart_dir + '\\', '')
                        key = rel
                        if key not in found:
                            found[key] = []
                        found[key].append(f'  L{i}: {stripped[:90]}')
                        break

print(f"Files with Uzbek text: {len(found)}\n")
for fpath, lines in sorted(found.items()):
    print(f"\n{fpath}:")
    for l in lines[:8]:
        print(l)
