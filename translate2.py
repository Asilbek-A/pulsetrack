#!/usr/bin/env python3
"""Second pass: replace all remaining Uzbek strings with English."""
import os
import sys

dart_dir = r"C:\Users\User\Desktop\whoop\whoop_app\lib"

# File-specific replacements (exact strings found in the scan)
file_replacements = {

    r"core\services\age_calculation_service.dart": [
        ("ortiqcha zo'riqish", "excessive strain"),
        ("Juda yuqori", "Very high"),
        ("yuqori", "high"),
        ("juda past", "very low"),
        ("past", "low"),
        ("normal", "normal"),
    ],

    r"features\activity\presentation\activity_main_screen.dart": [
        ("Todaygi strain", "Today's strain"),
        ("Todaygi qadam", "Today's steps"),
        ("Jami masofa", "Total distance"),
    ],

    r"features\activity\presentation\workout_summary_screen.dart": [
        ("Barcha foydalanuvchilarga", "All users"),
    ],

    r"features\age\presentation\age_screen.dart": [
        ("Qurilmani ulang", "Connect your device"),
        ("HR, HRV va uyqu ma'lumotlari yig'ila boshlaydi", "HR, HRV and sleep data will start collecting"),
        ("Qurilmani doimo kiyib yuring", "Keep wearing your device"),
        ("HR, HRV va uyqu ma'lumotlari avtomatik yig'iladi.", "HR, HRV and sleep data will be collected automatically."),
        ("HRV - Yurak variabelligi (33-kun avg)", "HRV - Heart Rate Variability (33-day avg)"),
        ("Yurak variabelligi (33-kun avg)", "Heart Rate Variability (33-day avg)"),
        ("Rest yurak urishi (33-kun avg)", "Resting Heart Rate (33-day avg)"),
        ("Uyqu davomiyligi (33-kun avg)", "Sleep Duration (33-day avg)"),
        ("Kunlik qadam (33-kun avg)", "Daily Steps (33-day avg)"),
        ("Nafas tezligi (33-kun avg)", "Respiratory Rate (33-day avg)"),
        ("Siz haqiqiy yoshingizdan ancha yoshroq ko'rinasiz. Sog'lom turmush tarzi, yaxshi uyqu v",
         "Your biological age is significantly lower than your chronological age. Keep up the great"),
        ("Biological Ageingiz haqiqiy yoshingizdan biroz past. Davom eting",
         "Your biological age is slightly below your chronological age. Keep going"),
        ("kichik yaxshilanishlar", "small improvements"),
        ("yoshroq ko'rinasiz", "younger than your age"),
        ("haqiqiy yoshingizdan", "than your chronological age"),
    ],

    r"features\community\presentation\community_screen.dart": [
        ("child: const Text('Bekor')", "child: const Text('Cancel')"),
        ("'Bekor'", "'Cancel'"),
    ],

    r"features\device\presentation\device_screen.dart": [
        ("'Qurilmani qidiring'", "'Search for device'"),
        ("Qurilmani qidiring", "Search for device"),
    ],

    r"features\health\presentation\health_screen.dart": [
        ("metricName: 'Nafas Olish'", "metricName: 'Respiratory Rate'"),
        ("'Nafas Olish'", "'Respiratory Rate'"),
        ("Nafas Olish", "Respiratory Rate"),
    ],

    r"features\home\presentation\home_screen.dart": [
        ("Strain ko'rinishi uchun yurak urishi ma'lumotlari yetarli bo'lishi va days davomida ye",
         "Strain requires sufficient heart rate data collected over several days"),
        ("Qurilmani taqib, odatdagidek kunlik harakat qiling",
         "Wear your device and go about your daily activity"),
        ("keyingi kunlarda Strain & Recovery grafigi to'ldiriladi.",
         "Strain & Recovery charts will fill in over the next few days."),
        ("'Uyqu sozlamalari'", "'Sleep Settings'"),
        ("Uyqu sozlamalari", "Sleep Settings"),
        ("'Uyqu sozlamalari saqlandi!'", "'Sleep settings saved!'"),
        ("Uyqu sozlamalari saqlandi!", "Sleep settings saved!"),
        ("Shaxsiylashtirilgan uyqu tavsiyalari 14 kunlik ma'lumot asosida hisoblanadi. Qurilmangizni kiyib turing.",
         "Personalized sleep recommendations are calculated from 14 days of data. Keep wearing your device."),
        ("Birinchi to'liq uyqudan keyin Recovery ko'rsatkichi ochiladi. HRV, R",
         "Recovery unlocks after your first complete sleep. Calculated from HRV, R"),
        ("Qurilmani taqib, kamida bir necha daqiqa yurish/yugurish bilan davom eting",
         "Wear your device and walk or jog for a few minutes"),
        ("shundan so'ng", "to start seeing"),
    ],

    r"features\journal\presentation\journal_screen.dart": [
        ("child: const Text('Bekor')", "child: const Text('Cancel')"),
        ("'Bekor'", "'Cancel'"),
    ],

    r"features\permissions\presentation\permissions_screen.dart": [
        ("Running va yurish masofasini o'lchash uchun", "To measure running and walking distance"),
    ],

    r"features\plan\presentation\plan_screen.dart": [
        ("child: const Text('Bekor')", "child: const Text('Cancel')"),
        ("'Bekor'", "'Cancel'"),
    ],

    r"features\profile\presentation\profile_screen.dart": [
        ("title: const Text('Uyqu eslatmasi')", "title: const Text('Sleep Reminder')"),
        ("'Uyqu eslatmasi'", "'Sleep Reminder'"),
        ("Uyqu eslatmasi", "Sleep Reminder"),
        ("title: 'Uyqu davomiyligi'", "title: 'Sleep Duration'"),
        ("'Uyqu davomiyligi'", "'Sleep Duration'"),
        ("Uyqu davomiyligi", "Sleep Duration"),
        ("Uyqu, tiklanish, yuklama va boshqa ko'rsatkichlarni real vaqtda kuzating.",
         "Track sleep, recovery, strain, and other metrics in real time."),
        ("child: const Text('Bekor')", "child: const Text('Cancel')"),
        ("'Bekor'", "'Cancel'"),
    ],

    r"features\recovery\presentation\recovery_detail_screen.dart": [
        ("metricName: 'Nafas Olish'", "metricName: 'Respiratory Rate'"),
        ("'Nafas Olish'", "'Respiratory Rate'"),
        ("Nafas Olish", "Respiratory Rate"),
    ],

    r"features\sleep\presentation\sleep_detail_screen.dart": [
        ("Uyqu paytida yurak urishi tezligi pasayadi. Low yurak urishi yaxshi dam olishni bildiradi",
         "Heart rate naturally decreases during sleep. A lower heart rate indicates better recovery"),
        ("Deep Sleep tanani tiklaydigan eng muhim bosqich. Muskullar va to'qimalar tiklanadi.",
         "Deep Sleep is the most restorative stage. Muscles and tissues repair and grow."),
        ("REM Sleep miyani tiklaydigan va xotira mustahkamlaydigan bosqich. Tushlar ko'rish bu bosqich",
         "REM Sleep restores the brain and consolidates memories. Dreaming occurs during this stage"),
        ("Uyquda $wakeEvents marta uyg'ongansiz. Ideal: 10 dan kam.",
         "You woke up $wakeEvents times during sleep. Ideal: fewer than 10."),
        ("Uyqu stress darajasi yurak urish tezligi va HRV asosida hisoblanadi. Low stress yaxshi uy",
         "Sleep stress is calculated from heart rate and HRV. Low stress indicates better sleep qual"),
        ("Sleep Qualityni yaxshilash uchun erta yotish va muntazam uyqu rejimini saqlash tavsiya",
         "To improve Sleep Quality, try going to bed earlier and maintaining a consistent sleep sched"),
        ("Sleep Qualityni yanada yaxshilash uchun stress darajasini kamaytirish, uyqu oldidan rel",
         "To further improve Sleep Quality, reduce stress, avoid screens before bed, and maintain a rel"),
    ],

    r"features\territories\presentation\my_territories_screen.dart": [
        ("'Jami masofa'", "'Total distance'"),
        ("Jami masofa", "Total distance"),
    ],

    r"features\territories\presentation\territory_leaderboard_screen.dart": [
        ("'Jami masofa'", "'Total distance'"),
        ("Jami masofa", "Total distance"),
    ],
}

# Global replacements applied to ALL files
global_replacements = [
    ("'Bekor'", "'Cancel'"),
    ('"Bekor"', '"Cancel"'),
    ("Nafas Olish", "Respiratory Rate"),
    ("Yurak urishi", "Heart Rate"),
    ("Uyqu sifati", "Sleep Quality"),
    ("Uyqu davomiyligi", "Sleep Duration"),
    ("Uyqu samaradorligi", "Sleep Efficiency"),
    ("Uyqu eslatmasi", "Sleep Reminder"),
    ("Uyqu sozlamalari", "Sleep Settings"),
    ("Jami masofa", "Total distance"),
    ("Todaygi", "Today's"),
    ("Nafas tezligi", "Respiratory Rate"),
    ("Kunlik qadam", "Daily Steps"),
]

changed = []

for root, dirs, files in os.walk(dart_dir):
    for fname in files:
        if not fname.endswith('.dart'):
            continue
        path = os.path.join(root, fname)
        rel = path.replace(dart_dir + '\\', '')

        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        original = content

        # File-specific
        if rel in file_replacements:
            for old, new in file_replacements[rel]:
                content = content.replace(old, new)

        # Global
        for old, new in global_replacements:
            content = content.replace(old, new)

        if content != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            changed.append(rel)

print(f"Updated {len(changed)} files:")
for f in changed:
    print(f"  {f}")
print("\nDone!")
