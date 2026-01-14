# 🧪 PulseTrack Test Qo'llanmasi

## 📱 APK O'rnatish

### 1. APK faylni topish
APK tayyor bo'lgach, bu manzilda bo'ladi:
```
C:\Users\User\Desktop\whoop\whoop_app\build\app\outputs\flutter-apk\app-release.apk
```

### 2. Telefonga o'tkazish
**Variant A: USB orqali**
```bash
# USB bilan telefoni kompyuterga ulang
# APK ni telefon Downloads papkasiga ko'chiring
```

**Variant B: Google Drive / Telegram / Email**
- APK ni yuklang
- Telefonda yuklab oling

### 3. O'rnatish
1. Telefonda **Downloads** ga o'ting
2. `app-release.apk` ni toping
3. **Install** bosing
4. Agar "Unknown sources" xabari chiqsa:
   - Settings → Security → Unknown sources → Allow

---

## 🔐 Dastlabki sozlash

### Backend serverni ishga tushirish
Telefon Wi-Fi orqali kompyuterga ulangan bo'lishi kerak:

1. **Kompyuter IP manzilini aniqlash:**
```bash
ipconfig
# IPv4 Address ni toping, masalan: 192.168.1.100
```

2. **Backend'da CORS sozlash** (agar kerak bo'lsa)
Backend allaqachon `cors` middleware yoqilgan, ishlashi kerak.

3. **Flutter API_CLIENT ni yangilash** (agar kerak bo'lsa):
```dart
// whoop_app/lib/core/api_client.dart
baseUrl: 'http://192.168.1.100:4000'  // Kompyuter IP
```

4. **Backend ishga tushirish:**
```bash
cd C:\Users\User\Desktop\whoop\backend
npm run dev
```

---

## 🧪 Test stsenariylari

### Test 1: Autentifikatsiya ✅

**Qadamlar:**
1. Ilovani oching
2. Login screen ko'rinadi
3. Email: `admin@pulsetrack.com`
4. Parol: `Admin123!`
5. **Login** bosing

**Kutilgan natija:**
- ✅ Login muvaffaqiyatli
- ✅ Home screen ochiladi
- ✅ Recovery/Strain/Sleep doiralari ko'rinadi

---

### Test 2: Qurilma ulanish (QR orqali) ✅

**Tayyorgarlik:**
- Huawei Band'ni to'liq zaryadlang
- Bluetooth yoqing
- Kamera ruxsatini bering

**Qadamlar:**
1. **Device** (yashil FAB tugma yoki top-right corner watch icon)
2. **QR Skan** tugmasini bosing
3. Kamera ruxsatini bering
4. Huawei Band qutisidagi QR kodni skanerlang

**Kutilgan natija:**
- ✅ QR kod o'qildi
- ✅ MAC address ajratildi
- ✅ "Avtomatik ulanish..." xabari
- ✅ Qurilma topildi va ulandi
- ✅ "Connected" badge ko'rinadi

**Agar QR kod yo'q bo'lsa:**
1. **Qidirish** tugmasini bosing
2. Ro'yxatdan Huawei Band'ni toping
3. Qurilmani bosib ulaning

---

### Test 3: Real-time HR monitoring ✅

**Qadamlar:**
1. Huawei Band'ni ulang
2. Bandni qo'lingizga taxing
3. **Home** screen'da kutib turing

**Kutilgan natija:**
- ✅ "LIVE HR" banner ko'rinadi
- ✅ HR raqami real-time yangilanadi (masalan: 72 bpm)
- ✅ HRV ko'rsatiladi (masalan: 45 ms)
- ✅ Recovery/Strain avtomatik hisoblanadi

---

### Test 4: Sleep Analysis ✅

**Variant A: Haqiqiy uyqu ma'lumotlari**
1. Kechqurun Huawei Band'ni taxing
2. Uxlang
3. Ertalab ilovani oching
4. **Sleep** doirasini bosing

**Variant B: Test uchun**
1. **Sleep** doirasini bosing
2. Mock data ko'rsatiladi
3. Barcha bo'limlarni tekshiring:
   - Sleep Performance ring
   - Hours vs Needed
   - Sleep Efficiency
   - Last Night's Sleep (HR graph)
   - Restorative Sleep
   - Weekly Trends

**Kutilgan natija:**
- ✅ Sleep score hisoblanadi
- ✅ HR patternlardan sleep stages aniqlanadi
- ✅ Deep/Light/REM/Awake durations
- ✅ Grafiklar to'g'ri ko'rsatiladi

---

### Test 5: Health Dashboard ✅

**Qadamlar:**
1. Pastdagi **Health** tabni bosing
2. Barcha metrikalarni ko'ring

**Kutilgan natija:**
- ✅ Live Vitals:
  - Heart Rate (agar ulangan bo'lsa)
  - HRV
  - SpO2 (agar qurilma qo'llab-quvvatlasa)
  - Temperature (agar qurilma qo'llab-quvvatlasa)
  - Respiratory Rate
  - Stress Level
- ✅ Today's Stats:
  - Steps progress bar
  - Distance
  - Calories progress bar
  - Active Minutes
- ✅ Current Activity
- ✅ HR Zones distribution

---

### Test 6: Device Capabilities ✅

**Qadamlar:**
1. Turli xil fitness band'larni ulang
2. Device screen'da capabilities ko'ring

**Kutilgan natija:**
- Huawei Band 8:
  - ✅ HR, HRV, SpO2, Temp, Steps, Calories, Sleep, Stress, Resp
  - ✅ "9 ta" metrics
- Huawei Band 7:
  - ✅ HR, HRV, SpO2, Steps, Calories, Sleep, Stress
  - ✅ "7 ta" metrics (Temperature yo'q)
- Mi Band:
  - ✅ HR, HRV, Steps, Calories, Sleep
  - ✅ "5 ta" metrics

---

## 🐛 Debug

### BLE ulanmasa:

1. **Bluetooth yoqilganligini tekshiring**
2. **Location (GPS) yoqing** - Android BLE scan uchun kerak
3. **App permissions:**
   - Settings → Apps → PulseTrack → Permissions
   - Location: Allow
   - Bluetooth: Allow
   - Camera: Allow (QR uchun)

4. **Qurilmani qayta ishga tushiring**

### Backend ulanmasa:

1. **IP manzilni tekshiring:**
```bash
ipconfig
# WiFi adapter IP ni toping
```

2. **API_CLIENT'ni yangilang:**
```dart
// whoop_app/lib/core/api_client.dart
baseUrl: 'http://192.168.X.X:4000'  // O'z IP
```

3. **Rebuild qiling:**
```bash
flutter build apk --release
```

### Xatoliklar log'ini ko'rish:

```bash
# Telefon ulangan holda
flutter logs
# yoki
adb logcat | findstr "flutter"
```

---

## 📈 Performance Test

### 1. Battery Test
- Bandni 8 soat taxib yuring
- Battery usage'ni tekshiring (Settings → Battery)

### 2. Accuracy Test
- HR ni boshqa ilova bilan solishtiring (Huawei Health)
- Steps ni oddiy sanagich bilan solishtiring

### 3. Connectivity Test
- Bluetooth o'chirib-yoqish
- Internet yo'q holatda ishlash
- Background'da ishlash

---

## ✅ Success Criteria

Quyidagilar ishlashi kerak:

- [x] Login/Register
- [x] Bluetooth device scan
- [x] QR code scanner
- [x] Auto-connect to device
- [x] Real-time HR display
- [x] HRV calculation
- [x] Recovery score calculation
- [x] Strain score calculation
- [x] Sleep analysis
- [x] Device capabilities detection
- [x] Health dashboard
- [x] Beautiful WHOOP-like UI
- [x] Bottom navigation
- [x] Dark theme

---

## 🎯 APK Tayyor bo'lgach:

1. `C:\Users\User\Desktop\whoop\whoop_app\build\app\outputs\flutter-apk\app-release.apk` ni toping
2. Telefonga o'tkazing
3. O'rnating
4. Test qiling!

**Barcha algoritmlar va BLE integratsiya tayyor! 🚀**

