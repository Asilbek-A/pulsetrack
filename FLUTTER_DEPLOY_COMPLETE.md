# 📱 Flutter Frontend Deploy - To'liq Qo'llanma

## 🎯 Eng Yaxshi Variantlar:

### 1. 🥇 Firebase Hosting (TAVSIYA)
- ✅ 100% Free
- ✅ Uyqu rejimi YO'Q
- ✅ CDN (tez)
- ✅ SSL avtomatik
- ✅ Stabil

### 2. 🥈 Vercel
- ✅ 100% Free
- ✅ Uyqu rejimi YO'Q
- ✅ GitHub integration
- ✅ Stabil

### 3. 🥉 Netlify
- ✅ 100% Free
- ✅ Uyqu rejimi YO'Q
- ✅ GitHub integration
- ✅ Stabil

---

## 🚀 Firebase Hosting (Eng Yaxshi)

### QADAM 1: Firebase Project

1. https://firebase.google.com → "Get started"
2. "Add project" → `pulsetrack`
3. Google Analytics: Optional
4. "Create project"

### QADAM 2: Firebase CLI

```powershell
npm install -g firebase-tools
firebase login
```

### QADAM 3: Firebase Init

```powershell
cd whoop_app
firebase init hosting
```

Tanlang:
- ✅ Use an existing project
- ✅ Project: `pulsetrack`
- ✅ Public directory: `build/web`
- ✅ Single-page app: Yes
- ✅ GitHub Actions: No

### QADAM 4: Build va Deploy

```powershell
flutter build web --release --base-href / --web-renderer canvaskit
firebase deploy --only hosting
```

### QADAM 5: URL Olish

Deploy tugagach:
- `https://pulsetrack.web.app`
- `https://pulsetrack.firebaseapp.com`

---

## ⚡ Vercel (Ikkinchi Variant)

### QADAM 1: Vercel'da Ro'yxatdan O'tish

1. https://vercel.com → GitHub orqali login
2. "Add New Project"
3. Repository: `Asilbek-A/pulsetrack`

### QADAM 2: Build Settings

- **Root Directory**: `whoop_app`
- **Build Command**: `flutter build web --release --base-href / --web-renderer canvaskit`
- **Output Directory**: `build/web`
- **Install Command**: `flutter pub get`

### QADAM 3: Deploy

"Deploy" bosing - avtomatik deploy qiladi!

URL: `https://pulsetrack.vercel.app`

---

## 🌐 Netlify (Uchinchi Variant)

### QADAM 1: Netlify'da Ro'yxatdan O'tish

1. https://netlify.com → GitHub orqali login
2. "Add new site" → "Import an existing project"

### QADAM 2: Build Settings

- **Base directory**: `whoop_app`
- **Build command**: `flutter build web --release --base-href / --web-renderer canvaskit`
- **Publish directory**: `whoop_app/build/web`

### QADAM 3: Deploy

"Deploy site" bosing - avtomatik deploy qiladi!

URL: `https://pulsetrack.netlify.app`

---

## 📱 Mobile APK Distribution

### Firebase App Distribution (Free)

1. Firebase Console → App Distribution
2. APK yuklash: `whoop_app/build/app/outputs/flutter-apk/app-release.apk`
3. Testers qo'shish
4. Avtomatik yuboriladi

### Direct APK Download

APK'ni server'da saqlash va download link berish.

---

## 🔗 API URL Sozlash

Flutter app'da production API URL'ni sozlash:

```powershell
# Firebase Hosting uchun
flutter build web --release --dart-define=API_BASE_URL=https://pulsetrack-api.onrender.com

# Vercel uchun
flutter build web --release --dart-define=API_BASE_URL=https://pulsetrack-api.onrender.com

# Netlify uchun
flutter build web --release --dart-define=API_BASE_URL=https://pulsetrack-api.onrender.com
```

---

## ✅ TAYYOR!

Barcha konfiguratsiyalar tayyor:
- ✅ `firebase.json` - Firebase Hosting
- ✅ `vercel.json` - Vercel
- ✅ `netlify.toml` - Netlify
- ✅ GitHub Actions workflow - Avtomatik deploy

**TAVSIYA**: Firebase Hosting eng yaxshi variant!
