# 🚀 GitHub'ga yuklash va Render.com'da deploy

## ✅ QADAM 1: Git repository tayyor (Bajarildi!)

Git repository yaratildi va barcha fayllar commit qilindi.

## 📤 QADAM 2: GitHub'ga yuklash

### 2.1. GitHub'da repository yarating:

1. https://github.com ga kiring
2. "New repository" tugmasini bosing
3. Repository nomi: `pulsetrack` (yoki istalgan nom)
4. **Description**: "WHOOP-style fitness tracking app"
5. **Public** qiling (Render.com bepul tier uchun kerak)
6. **"Initialize with README"** ni **O'CHIRING** (bizda allaqachon fayllar bor)
7. "Create repository" bosing

### 2.2. Lokal repository'ni GitHub'ga ulang:

GitHub'da repository yaratgandan keyin, quyidagi buyruqlarni bajaring:

```powershell
# GitHub'dan olingan URL'ni ishlating (YOUR_USERNAME o'rniga o'z username'ingizni qo'ying)
git remote add origin https://github.com/YOUR_USERNAME/pulsetrack.git
git branch -M main
git push -u origin main
```

**Misol:**
```powershell
git remote add origin https://github.com/johndoe/pulsetrack.git
git branch -M main
git push -u origin main
```

## 🌐 QADAM 3: Render.com'da deploy

### 3.1. Render.com'da ro'yxatdan o'ting:

1. https://render.com ga kiring
2. "Get Started for Free" tugmasini bosing
3. **"Sign up with GitHub"** ni tanlang
4. GitHub akkauntingizga ruxsat bering

### 3.2. Blueprint orqali deploy:

1. Render Dashboard'da **"New +"** tugmasini bosing
2. **"Blueprint"** ni tanlang
3. GitHub repository'ni tanlang: `pulsetrack`
4. **"Apply"** tugmasini bosing
5. 5-10 daqiqa kuting (build va deploy jarayoni)

### 3.3. Deploy natijasi:

Deploy tugagach:
- ✅ **Service URL**: `https://pulsetrack-api.onrender.com`
- ✅ **Database**: Avtomatik yaratildi va ulandi
- ✅ **Environment Variables**: Avtomatik sozlandi

## 📱 QADAM 4: Flutter App yangilash

Production API URL'ni olishdan keyin:

```powershell
cd whoop_app
flutter build apk --release --dart-define=API_BASE_URL=https://pulsetrack-api.onrender.com
```

## ✅ TAYYOR!

Endi sizning backend'ingiz production'da ishlamoqda!

---

## 🔧 Muammo bo'lsa:

1. **Git push xatosi**: GitHub'da repository yaratilganligini tekshiring
2. **Render deploy xatosi**: Dashboard → Logs'ni tekshiring
3. **Database xatosi**: Render Dashboard → Database → Connection String'ni tekshiring
