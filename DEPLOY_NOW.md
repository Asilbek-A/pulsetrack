# 🚀 TEZKOR DEPLOY - 5 DAQIQA

## 1. Git Repository Yaratish (Agar yo'q bo'lsa)

```bash
cd C:\Users\User\Desktop\whoop
git init
git add .
git commit -m "Initial commit - Ready for Render deployment"
```

## 2. GitHub'ga Yuklash

1. GitHub.com'ga kiring
2. "New repository" yarating
3. Repository nomi: `pulsetrack` (yoki istalgan)
4. **Public** qiling (Render.com bepul tier uchun)
5. Quyidagi buyruqlarni bajaring:

```bash
git remote add origin https://github.com/YOUR_USERNAME/pulsetrack.git
git branch -M main
git push -u origin main
```

## 3. Render.com'da Deploy

1. https://render.com ga kiring
2. "Get Started for Free" → GitHub orqali ro'yxatdan o'ting
3. Dashboard'da "New +" → **"Blueprint"** tanlang
4. GitHub repository'ni tanlang
5. "Apply" bosing
6. 5-10 daqiqa kuting

## 4. URL Olish

Deploy tugagach:
- Service URL: `https://pulsetrack-api.onrender.com`
- Bu sizning production API URL'ingiz!

## 5. Flutter App Yangilash

```bash
cd whoop_app
flutter build apk --release --dart-define=API_BASE_URL=https://pulsetrack-api.onrender.com
```

## ✅ TAYYOR!

Endi sizning backend'ingiz production'da ishlamoqda!
