## PulseTrack / WHOOP tipidagi fitness ilova

Bu loyiha WHOOP ga o‘xshash sog‘liq va fitness tracking tizimi uchun **Flutter mobil ilova** (`whoop_app`) va **Node.js backend** (`backend`) skeletidan iborat.

### Tuzilma

- `whoop_app/` – Flutter ilova:
  - Dark UI, 5 ta asosiy tab: Home, Sleep, Workouts, Health, Profile
  - Brasletni Bluetooth Low Energy (BLE) orqali qidirish va ulash uchun skeleton
  - Kelajakda backend API va haqiqiy dataga ulanish uchun tayyor
- `backend/` – Node.js (Express + TypeScript) minimal API:
  - Soddalashtirilgan `/health`, `/users/me`, `/metrics/health` endpointlari
  - Keyinchalik NestJS yoki to‘liq arxitekturaga kengaytirish uchun baza

### Ishga tushirish (Flutter)

```bash
cd whoop_app
flutter pub get
flutter run
```

### Ishga tushirish (Backend)

```bash
cd backend
npm install
npm run dev
```

Backend `http://localhost:4000` da ishlaydi.


