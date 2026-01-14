# ⚡ Vercel Deploy - Hozir

## ✅ Tayyorlangan fayllar:

1. ✅ `whoop_app/vercel.json` - Vercel konfiguratsiyasi
2. ✅ GitHub repository: https://github.com/Asilbek-A/pulsetrack
3. ✅ Barcha kodlar yuklangan

## 🚀 QADAM 1: Vercel'da Ro'yxatdan O'tish

1. https://vercel.com ga kiring
2. "Sign Up" bosing
3. **"Continue with GitHub"** ni tanlang
4. GitHub akkauntingizga ruxsat bering (Asilbek-A)

## 📦 QADAM 2: Project Yaratish

1. Vercel Dashboard'da **"Add New Project"** bosing
2. **"Import Git Repository"** ni tanlang
3. Repository tanlang: **`Asilbek-A/pulsetrack`**
4. **"Import"** bosing

## 🔧 QADAM 3: Build Settings

Vercel avtomatik `vercel.json` ni topadi, lekin quyidagilarni tekshiring:

- **Framework Preset**: Other
- **Root Directory**: `whoop_app` (agar kerak bo'lsa)
- **Build Command**: `flutter pub get && flutter build web --release --base-href / --web-renderer canvaskit`
- **Output Directory**: `build/web`
- **Install Command**: `flutter pub get`

**YOKI** `vercel.json` fayli mavjud, shuning uchun avtomatik sozlanadi!

## 🌐 QADAM 4: Environment Variables (Optional)

Agar kerak bo'lsa, **Environment Variables** qo'shing:
- `API_BASE_URL` = `https://pulsetrack-api.onrender.com` (backend URL)

## 🚀 QADAM 5: Deploy

**"Deploy"** bosing!

Vercel:
1. Flutter o'rnatadi
2. Dependencies o'rnatadi (`flutter pub get`)
3. Web build qiladi
4. Deploy qiladi

## ✅ NATIJA:

Deploy tugagach, sizga URL beriladi:
- `https://pulsetrack.vercel.app`
- Yoki custom domain (agar sozlagan bo'lsangiz)

## 🔄 Keyingi Deploy'lar:

Har safar GitHub'ga push qilsangiz, Vercel avtomatik yangi deploy qiladi!

---

## 📱 Mobile APK uchun:

Flutter web versiyasi Vercel'da ishlaydi. Mobile APK uchun:
- Firebase App Distribution (free)
- Yoki direct APK download

---

## ✅ TAYYOR!

Endi Vercel'da project yaratib, deploy qilishingiz mumkin!
