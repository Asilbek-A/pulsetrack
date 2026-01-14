# 🚀 PulseTrack - Render.com Deploy Guide

## ✅ Tayyorlangan fayllar:

1. ✅ `render.yaml` - Render.com avtomatik konfiguratsiya
2. ✅ `.gitignore` - Git uchun to'g'ri sozlangan
3. ✅ `backend/.gitignore` - Backend uchun
4. ✅ `backend/env.example` - Environment variables template
5. ✅ Backend production-ready (NODE_ENV check, CORS, database sync)

## 📋 Deploy qilish (3 qadam):

### QADAM 1: Git Repository

```powershell
# PowerShell'da:
cd C:\Users\User\Desktop\whoop
git init
git add .
git commit -m "Ready for Render deployment"
```

### QADAM 2: GitHub'ga yuklash

1. GitHub.com → New repository
2. Repository nomi: `pulsetrack`
3. **Public** qiling
4. Quyidagi buyruqlarni bajaring:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/pulsetrack.git
git branch -M main
git push -u origin main
```

### QADAM 3: Render.com'da deploy

1. https://render.com → "Get Started for Free"
2. GitHub orqali ro'yxatdan o'ting
3. Dashboard → "New +" → **"Blueprint"**
4. Repository'ni tanlang
5. "Apply" bosing
6. 5-10 daqiqa kuting

## 🎯 Natija:

Deploy tugagach, sizga URL beriladi:
- `https://pulsetrack-api.onrender.com`

Bu sizning production API URL'ingiz!

## 📱 Flutter App yangilash:

```powershell
cd whoop_app
flutter build apk --release --dart-define=API_BASE_URL=https://pulsetrack-api.onrender.com
```

## ⚠️ Muhim eslatmalar:

1. **Database**: Render.com avtomatik PostgreSQL yaratadi
2. **Environment Variables**: `render.yaml` orqali avtomatik sozlanadi
3. **JWT_SECRET**: Avtomatik generate qilinadi
4. **CORS**: Hozircha `*` (keyin production'da o'zgartirish mumkin)
5. **Free Tier**: 750 soat/oy, 15 daqiqadan keyin "uyqu" rejimi

## 🔧 Muammo bo'lsa:

1. Render.com Dashboard → Logs'ni tekshiring
2. Database connection tekshiring
3. Environment variables tekshiring

---

**Tayyor!** Endi sizning backend'ingiz production'da ishlamoqda! 🎉
