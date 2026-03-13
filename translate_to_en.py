#!/usr/bin/env python3
"""Translate all Uzbek strings to English in all dart files."""
import os

replacements = [
    # metric descriptions in home_screen
    ("Shaxsiylashtirilgan uyqu tavsiyalari 14 kunlik ma'lumot asosida hisoblanadi. Qurilmangizni kiyib turing.",
     "Personalized sleep recommendations are calculated from 14 days of data. Keep wearing your device."),
    ("Birinchi to'liq uyqudan keyin Recovery ko'rsatkichi ochiladi. HRV, RHR va uyqu asosida hisoblanadi.",
     "Recovery unlocks after your first complete sleep. Calculated from HRV, resting HR, and sleep quality."),
    ("Kunlik kardiovaskular yuklanma. Qurilma kiyilgandan boshlab real vaqtda hisoblanadi.",
     "Daily cardiovascular load. Tracked in real-time from the moment you put on your device."),

    # home_screen info messages
    ("Qurilma ulanmagan", "Device not connected"),
    ("Ma'lumotlarni olish uchun fitness qurilmangizni ulang.", "Connect your fitness device to start collecting data."),
    ("Ma'lumotlar yo'q", "No data yet"),
    ("Ma'lumotlarni yig'ishni boshlash uchun qurilmangizni taqing.", "Put on your device to start collecting data."),
    ("Ma'lumotlar yetarli emas", "Not enough data yet"),
    ("To'liq tahlil uchun kamida 3 kunlik ma'lumot kerak. Hozir ", "Need at least 3 days of data for full analysis. Currently "),
    (" kunlik ma'lumot bor.", " days of data collected."),

    # health_screen milestones
    ("Biologik Yosh", "Biological Age"),

    # calibration phases
    ("Boshlang'ich bosqich", "Getting started"),
    ("Asosiy bosqich", "Building baseline"),
    ("Ilg'or bosqich", "Calibrating"),
    ("Yakuniy bosqich", "Finalizing"),
    ("To'liq kalibrlangan", "Fully calibrated"),
    ("Kalibrlanyapti...", "Calibrating..."),
    ("Kalibrlanyapti", "Calibrating"),

    # health_screen calibration banner
    ("Recovery & HRV bosqichi", "Recovery & HRV phase"),
    ("kun qoldi", "days remaining"),
    ("kun ichida", "days of"),
    (" kun ", " days "),
    (" kun.", " days."),

    # recovery screen
    ("Kalibrlash davom etmoqda", "Calibration in progress"),
    ("Tiklnish ko'rsatkichi", "Recovery Score"),
    ("Uyqu sifati", "Sleep Quality"),
    ("Tana faolligi", "Physical Activity"),

    # sleep screen - sleep coach
    ("Ajoyib uyqu", "Great sleep"),
    ("Yetarli uyqu", "Adequate sleep"),
    ("Uyqu qarzi oshmoqda", "Sleep debt building"),
    ("Tavsiya etilgan yotish vaqti", "Suggested bedtime"),

    # profile screen
    ("Sozlamalar", "Settings"),
    ("Profil", "Profile"),
    ("Chiqish", "Sign Out"),
    ("Tahrirlash", "Edit"),
    ("Saqlash", "Save"),
    ("Bekor qilish", "Cancel"),
    ("Maqsad", "Goal"),
    ("Maqsadlar", "Goals"),
    ("Hisobim", "My Account"),
    ("Parolni o'zgartirish", "Change Password"),
    ("Bildirishnomalar", "Notifications"),
    ("Maxfiylik", "Privacy"),
    ("Yordam", "Help"),
    ("Ilovani baholash", "Rate App"),
    ("Versiya", "Version"),
    ("Tizimdan chiqish", "Log Out"),
    ("Haqida", "About"),
    ("Statistika", "Statistics"),

    # activity screen
    ("Mashg'ulot", "Workout"),
    ("Mashg'ulotlar", "Workouts"),
    ("Faoliyat", "Activity"),
    ("Faoliyatlar", "Activities"),
    ("Yugurish", "Running"),
    ("Velosiped", "Cycling"),
    ("Suzish", "Swimming"),
    ("Yurish", "Walking"),
    ("Mashq", "Exercise"),
    ("Boshlash", "Start"),
    ("Tugatish", "Finish"),
    ("To'xtatish", "Stop"),
    ("Davom ettirish", "Resume"),
    ("Kaloriya", "Calories"),
    ("Qadam", "Steps"),
    ("Masofa", "Distance"),
    ("Vaqt", "Duration"),
    ("Tezlik", "Speed"),
    ("O'rtacha yurak urishi", "Avg Heart Rate"),
    ("Maksimal yurak urishi", "Max Heart Rate"),

    # device screen
    ("Qurilmani ulash", "Connect Device"),
    ("Qurilma topilmadi", "No device found"),
    ("Ulanmoqda", "Connecting"),
    ("Ulangan", "Connected"),
    ("Ulanmagan", "Disconnected"),
    ("Batareya", "Battery"),
    ("Signal kuchi", "Signal Strength"),
    ("Sinxronlash", "Sync"),
    ("Yangilash", "Update"),

    # setup/permissions screens
    ("Keyingi", "Next"),
    ("Orqaga", "Back"),
    ("Ruxsat berish", "Allow"),
    ("Ruxsat yo'q", "Permission denied"),
    ("Joylashuv", "Location"),
    ("Bluetooth", "Bluetooth"),
    ("Jismoniy faoliyat", "Physical Activity"),
    ("Sog'liq ma'lumotlari", "Health Data"),

    # community screen
    ("Jamiyat", "Community"),
    ("Do'stlar", "Friends"),
    ("Liderlar jadvali", "Leaderboard"),
    ("Tabriklaymiz", "Congratulations"),
    ("Yuborish", "Send"),
    ("Izoh", "Comment"),
    ("Izohlar", "Comments"),
    ("Yoqtirish", "Like"),

    # gps screen
    ("Joylashuv kuzatish", "Location Tracking"),
    ("Marshrut", "Route"),
    ("Tezlik", "Speed"),

    # journal screen
    ("Kundalik", "Journal"),
    ("Qayd", "Note"),
    ("Qo'shish", "Add"),
    ("Tahrirlash", "Edit"),
    ("O'chirish", "Delete"),
    ("Bugun", "Today"),
    ("Kecha", "Yesterday"),
    ("Hech narsa yo'q", "Nothing here yet"),

    # plan screen
    ("Reja", "Plan"),
    ("Mening rejam", "My Plan"),
    ("Haftalik reja", "Weekly Plan"),
    ("Dam olish", "Rest"),
    ("Faol dam olish", "Active Recovery"),
    ("Intensiv mashq", "High Intensity"),

    # general
    ("Yurak urishi", "Heart Rate"),
    ("Nafas olish tezligi", "Respiratory Rate"),
    ("Qon bosimi", "Blood Pressure"),
    ("Harorat", "Temperature"),
    ("Uxlash", "Sleep"),
    ("Uyg'onish", "Wake"),
    ("REM uyqu", "REM Sleep"),
    ("Chuqur uyqu", "Deep Sleep"),
    ("Yengil uyqu", "Light Sleep"),
    ("Uyqu samaradorligi", "Sleep Efficiency"),
    ("Uyqu muddati", "Sleep Duration"),
    ("Kerakli uyqu", "Sleep Need"),
    ("Uyqu qarzi", "Sleep Debt"),
    ("Tiklnish", "Recovery"),
    ("Zo'riqish", "Strain"),
    ("Sog'liq", "Health"),
    ("Biologik yosh", "Biological Age"),
    ("Xronologik yosh", "Chronological Age"),
    ("Yosh", "Age"),
    ("Yoshroq", "Younger"),
    ("Kattaroq", "Older"),
    ("Yaxshi", "Good"),
    ("O'rtacha", "Moderate"),
    ("Yomon", "Poor"),
    ("Ajoyib", "Excellent"),
    ("Yuqori", "High"),
    ("Past", "Low"),
    ("Normal", "Normal"),
    ("Diqqat", "Attention"),
    ("Ogohlantirish", "Warning"),
    ("Xato", "Error"),
    ("Muvaffaqiyatli", "Success"),
    ("Yuklanmoqda", "Loading"),
    ("Iltimos kuting", "Please wait"),
    ("Qayta urinib ko'ring", "Try again"),
    ("Internetga ulanish yo'q", "No internet connection"),
    ("Serverga ulanib bo'lmadi", "Could not connect to server"),
    ("Noma'lum xato", "Unknown error"),

    # Keep these English as-is (no change needed)
    # "Recovery", "Strain", "Sleep", "HRV", "SpO2", etc.
]

dart_dir = r"C:\Users\User\Desktop\whoop\whoop_app\lib"
changed_files = []

for root, dirs, files in os.walk(dart_dir):
    for fname in files:
        if fname.endswith('.dart'):
            path = os.path.join(root, fname)
            try:
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                original = content
                for old, new in replacements:
                    if old in content:
                        content = content.replace(old, new)
                if content != original:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    changed_files.append(path)
            except Exception as e:
                print(f"ERROR {path}: {e}")

print(f"\nUpdated {len(changed_files)} files:")
for f in changed_files:
    print(f"  {f.replace(dart_dir, 'lib')}")
print("\nDone!")
