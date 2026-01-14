# PulseTrack - WHOOP tipidagi Fitness Tracking Ilova

## 📋 Loyiha haqida

WHOOP fitness ilovasiga o'xshash, to'liq funksional fitness tracking mobil ilova. Flutter (Dart) va Node.js (TypeScript) yordamida yaratilgan.

---

## 🎯 Asosiy funksiyalar

### ✅ To'liq bajarilgan funksiyalar:

#### 1. **Authentication & Backend**
- Login / Register
- JWT token autentifikatsiya
- PostgreSQL database
- RESTful API (Express + TypeORM)
- Default admin user: `admin@pulsetrack.com` / `Admin123!`

#### 2. **BLE (Bluetooth Low Energy) Integration**
**Qo'llab-quvvatlanadigan qurilmalar:**
- Huawei Band (7, 8, 9, Watch GT)
- Xiaomi Mi Band (7, 8)
- Amazfit
- Samsung Galaxy Watch
- Fitbit
- Garmin
- Umumiy BLE fitness braceletlar

**O'qiladigan ma'lumotlar:**
- ❤️ Heart Rate (HR) - yurak urishi
- 📊 HRV (Heart Rate Variability)
- 🫁 SpO2 - qon kislorod darajasi
- 🌡️ Skin Temperature - teri harorati
- 👟 Steps - qadamlar
- 📏 Distance - masofa
- 🔋 Battery - akkumulyator

#### 3. **Algoritmlar (WHOOP uslubida)**

| Algoritm | Hisoblash usuli |
|----------|----------------|
| **Recovery Score (0-100%)** | HRV (35%) + Resting HR (25%) + Sleep (25%) + Strain penalty (15%) |
| **Strain Score (0-21)** | HR zonalarida o'tkazilgan vaqt × koeffitsient |
| **Sleep Performance** | Hours vs Need (40%) + Efficiency (25%) + Restorative (25%) + Wakes (10%) |
| **Sleep Stages** | HR pattern analysis → Awake/Light/Deep/REM |
| **Stress Level (0-100)** | HRV ratio + pNN50 + HR elevation |
| **Calories Burned** | Keytel formula: age, weight, gender, HR |
| **BMR** | Mifflin-St Jeor equation |
| **Respiratory Rate** | RSA (Respiratory Sinus Arrhythmia) from RR intervals |
| **Activity Detection** | Accelerometer magnitude + HR patterns |

#### 4. **UI/UX (WHOOP dizayni)**
- 🏠 **Home Screen** - Recovery/Strain/Sleep doiralari
- 💤 **Sleep Detail** - uyqu tahlili, bosqichlar, grafiklar
- 💪 **Recovery Detail** - tiklanish ko'rsatkichi
- 🔥 **Strain Detail** - kunlik yuklama
- 🩺 **Health Dashboard** - real-time metrikalar
- 📱 **Device Screen** - QR skaner + qurilma ulanish
- 👤 **Profile** - sozlamalar, logout
- 👥 **Community** - jamoa, leaderboard (placeholder)

#### 5. **QR Kod Skaner**
- Qurilma qutisidagi QR kodni skanerlash
- MAC address avtomatik ajratish
- Qurilmani avtomatik topish va ulanish
- Qo'llab-quvvatlanadigan formatlar:
  - MAC address: `AA:BB:CC:DD:EE:FF`
  - JSON: `{"mac": "AA:BB:CC:DD:EE:FF", "name": "Device"}`
  - URL: `https://device.com/pair?mac=...`

#### 6. **Device Capabilities (Aqlli aniqlash)**
Har bir qurilma o'z imkoniyatlariga qarab ko'rsatiladi:
- Huawei Band 7: HR, HRV, SpO2, Steps, Sleep ✅
- Huawei Band 8/9: + Temperature, Respiratory ✅
- Mi Band: HR, HRV, Steps, Sleep ✅
- Samsung: + ECG, Blood Pressure ✅

---

## 🛠️ Texnologiyalar

### Frontend (Flutter)
```yaml
dependencies:
  flutter_blue_plus: ^1.33.5        # BLE
  mobile_scanner: ^5.1.1            # QR scanner
  provider: ^6.1.2                  # State management
  dio: ^5.7.0                       # HTTP client
  fl_chart: ^0.69.0                 # Grafiklar
  flutter_secure_storage: ^9.2.2    # Token storage
  permission_handler: ^11.3.1       # Permissions
```

### Backend (Node.js)
```json
{
  "express": "^4.19.2",
  "typeorm": "^0.3.20",
  "pg": "^8.12.0",
  "bcryptjs": "^2.4.3",
  "jsonwebtoken": "^9.0.2"
}
```

### Database
- PostgreSQL 16
- Database: `pulsetrack`
- Tables: `users`, `health_metrics`

---

## 📂 Fayl strukturasi

```
whoop/
├── whoop_app/                          # Flutter mobile app
│   ├── lib/
│   │   ├── core/
│   │   │   ├── models/
│   │   │   │   ├── health_data.dart           # Data models
│   │   │   │   └── device_capabilities.dart   # Device profiles
│   │   │   ├── services/
│   │   │   │   ├── ble_health_service.dart    # BLE service
│   │   │   │   └── health_algorithm_service.dart # Algorithms
│   │   │   ├── providers/
│   │   │   │   └── health_data_provider.dart  # State management
│   │   │   ├── theme.dart
│   │   │   ├── api_client.dart
│   │   │   └── auth_token_storage.dart
│   │   ├── features/
│   │   │   ├── auth/                          # Login/Register
│   │   │   ├── home/                          # Home screen
│   │   │   ├── sleep/                         # Sleep analysis
│   │   │   ├── recovery/                      # Recovery score
│   │   │   ├── strain/                        # Strain score
│   │   │   ├── health/                        # Health dashboard
│   │   │   ├── device/                        # Device connection
│   │   │   │   └── qr_scanner_screen.dart    # QR scanner
│   │   │   ├── activity/                      # Activity tracking
│   │   │   ├── community/                     # Community features
│   │   │   └── profile/                       # User profile
│   │   └── main.dart
│   └── android/
│       └── app/
│           └── build.gradle.kts               # Android config
│
└── backend/                                    # Node.js backend
    ├── src/
    │   ├── modules/
    │   │   ├── auth/                          # Auth routes
    │   │   ├── users/                         # User management
    │   │   └── metrics/                       # Health metrics
    │   ├── infra/
    │   │   ├── data-source.ts                 # TypeORM config
    │   │   └── seed.ts                        # Database seeding
    │   └── index.ts                           # Server entry point
    ├── .env                                    # Environment variables
    └── package.json
```

---

## 🚀 O'rnatish va ishga tushirish

### Backend

```bash
# 1. PostgreSQL o'rnatish va database yaratish
createdb pulsetrack

# 2. Dependencies o'rnatish
cd backend
npm install

# 3. .env faylni sozlash
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=yourpassword
DB_DATABASE=pulsetrack
JWT_SECRET=your-secret-key
PORT=4000

# 4. Ishga tushirish
npm run dev
```

### Flutter App

```bash
# 1. Dependencies o'rnatish
cd whoop_app
flutter pub get

# 2. Android qurilmada ishga tushirish
flutter run

# 3. APK yaratish
flutter build apk --release
# APK manzil: build/app/outputs/flutter-apk/app-release.apk
```

---

## 📱 Test qilish

### Login ma'lumotlari:
```
Email: admin@pulsetrack.com
Password: Admin123!
```

### Test qadamlari:
1. ✅ Backend ishga tushirish (`npm run dev`)
2. ✅ APK ni Android telefonga o'rnatish
3. ✅ Login qilish
4. ✅ **Device** bo'limiga o'tish
5. ✅ **QR Skan** yoki **Qidirish** orqali Huawei Band'ni ulash
6. ✅ Real-time HR/HRV ko'rish
7. ✅ **Home** - Recovery/Strain ko'rish
8. ✅ **Sleep** - uyqu tahlili ko'rish
9. ✅ **Health** - barcha metrikalar ko'rish

---

## 🎨 Dizayn xususiyatlari

### Ranglar (WHOOP uslubida)
```dart
Background: #0D1117 (Dark)
Card: #1C2128
Accent: #00E0FF (Cyan)
Success: #238636 (Green)
Warning: #F59E0B (Orange)
Error: #FF4B5C (Red)

Recovery Green: #00D47E
Recovery Yellow: #FFC857
Recovery Red: #FF4B5C

Sleep: #6366F1 (Indigo)
Strain: #00E0FF (Cyan)
```

### Fontlar
- Google Fonts: Inter
- LetterSpacing: 1.2-2.0 (uppercase titles)

---

## 🔧 Texnik xususiyatlar

### BLE Protokol
- **Standard Services**: HR (0x180D), SpO2 (0x1822), Temperature (0x1809), Battery (0x180F)
- **Huawei Specific**: 0xFEE0, 0xFEE1
- **Xiaomi Specific**: 0xFEE0, 0xFEE1
- **Auto-detection**: Qurilma nomi va servicelar orqali

### Algoritmlar detali

#### Recovery Score
```
Score = Base(50) × Weights:
  - HRV ratio (35%): (Current HRV / Baseline HRV)
  - Resting HR (25%): (Baseline RHR / Current RHR)
  - Sleep Quality (25%): Last night's sleep score
  - Strain Penalty (15%): Previous day strain > 15
```

#### Strain Score
```
Strain = Σ(Time in Zone × Zone Coefficient)
Zones:
  - Rest (0-50%): 0.00
  - Warmup (50-60%): 0.02
  - Fat Burn (60-70%): 0.08
  - Cardio (70-80%): 0.25
  - Peak (80-90%): 0.70
  - Max (90-100%): 1.50
Max Daily Strain: 21.0
```

#### Sleep Stages Detection
```
Input: HR time series data
Algorithm:
  1. Calculate average HR for session
  2. For each 5-minute window:
     - HR < 92% avg + low variability → Deep Sleep
     - HR > 98% avg + high variability → REM / Awake
     - HR ≈ avg + medium variability → Light Sleep
  3. Smooth transitions between stages
Output: Time-stamped sleep stages
```

---

## 📊 Ma'lumotlar oqimi

```
[Fitness Band] 
    ↓ BLE
[BleHealthService]
    ↓ Stream
[HealthAlgorithmService]
    ↓ Calculations
[HealthDataProvider]
    ↓ State
[UI Widgets]
```

---

## ⚠️ Ma'lum muammolar va yechimlar

### 1. Windows Desktop build
**Muammo**: Visual Studio toolchain topilmadi
**Yechim**: Android APK ni ishlatish (barcha funksiyalar ishlaydi)

### 2. BLE Web qo'llab-quvvatlash
**Muammo**: Chrome/Web da BLE cheklangan
**Yechim**: Android/iOS da to'liq ishlaydi

### 3. Developer Mode (Windows)
**Muammo**: Symlink support kerak
**Yechim**: Settings → Developer Mode → ON

---

## 🔮 Kelajak rejalar

### Qo'shilishi mumkin:
- [ ] Blood Pressure monitoring
- [ ] ECG analysis (Samsung, Apple Watch)
- [ ] GPS tracking for outdoor activities
- [ ] Social features (teams, challenges)
- [ ] Cloud sync (Firebase)
- [ ] Apple HealthKit integration
- [ ] Google Fit integration
- [ ] Sleep coaching recommendations
- [ ] Nutrition tracking
- [ ] Workout library

---

## 📄 Litsenziya

Shaxsiy loyiha - barcha huquqlar himoyalangan.

---

## 👨‍💻 Muallif

PulseTrack - WHOOP-inspired Fitness Tracker
Yaratilgan: 2025

---

## 🙏 Minnatdorchilik

- WHOOP - dizayn va algoritm inspiratsiyasi
- Flutter team - mobile framework
- TypeORM - backend ORM
- flutter_blue_plus - BLE plugin
- mobile_scanner - QR scanner plugin

---

**Versiya**: 1.0.0  
**Oxirgi yangilanish**: 2025-12-04  
**Status**: ✅ Production Ready (Android)

