#!/usr/bin/env python3
"""Find remaining Uzbek text in dart files."""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

uzbek_words = [
    'Boshlash', 'Tugatish', 'Davom', 'Tahrirlash', 'Saqlash', 'Bekor',
    'Maqsad', 'Hisobim', 'Bildirishnoma', 'Maxfiylik', 'Yordam', 'Haqida',
    'Bugun', 'Kecha', 'qadam',
    'Jamiyat', 'Liderlar',
    'Joylashuv',
    'Ulanmoqda', 'Ulanmagan',
    'Sinxron', 'Yuklanmoqda',
    'Qurilmani', 'qurilmangizni',
    'Hech narsa',
    'Tabriklaymiz', 'Yuborish',
    "ma'lumot",
    'oshmoqda',
    'bosqich',
    'Tiklnish', 'tiklnish',
    "Ko'rsatkich",
    "Qo'shish",
    "O'chirish",
    'Kundalik',
    'uyqu', 'Uyqu',
    'yurak', 'Yurak',
    'nafas', 'Nafas',
    'Masofa', 'masofa',
    'Batareya',
    'Versiya',
    'Izoh',
    'Yoqtirish',
    'Statistika',
    'Barcha foydalanuvchi',
    'qadam',
    'Todaygi',
    'bosqichi',
    'zo\'riqish',
    'Reja',
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
                        entry = f'  L{i}: {stripped[:90]}'
                        if entry not in found[key]:
                            found[key].append(entry)
                        break

print(f"Files with Uzbek text: {len(found)}\n")
for fpath, lines in sorted(found.items()):
    print(f"\n{fpath}:")
    for l in lines[:10]:
        try:
            print(l.encode('ascii', errors='replace').decode('ascii'))
        except:
            pass
