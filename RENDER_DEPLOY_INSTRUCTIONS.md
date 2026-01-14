# 🚀 Render.com - Professional Dеплой (O'zbek tilida)

**Bepul serverga professional o'rnatish**

---

## 📋 Boshlashdan oldin

### Kerakli narsalar:
- ✅ Git repository (GitHub, GitLab yoki Bitbucket)
- ✅ Render.com account (bepul)
- ✅ 15-20 daqiqa vaqt

---

## 🎯 1-qadam: Git Repository tayyorlash

### Agar kod hali Git'da bo'lmasa:

```bash
cd C:\Users\User\Desktop\whoop

# Git init (agar yo'q bo'lsa)
git init

# Barcha fayllarni qo'shish
git add .

# Commit qilish
git commit -m "Ready for Render deployment"

# GitHub'ga yuklash (yoki GitLab/Bitbucket)
# GitHub'da yangi repository yarating, keyin:
git remote add origin https://github.com/yourusername/pulsetrack.git
git push -u origin main
```

---

## 🌐 2-qadam: Render.com'da ro'yxatdan o'tish

1. **Render.com'ga kiring:** https://render.com
2. **"Get Started for Free"** tugmasini bosing
3. **GitHub/GitLab/Bitbucket** orqali ro'yxatdan o'ting
4. **Repositoriyani ulang** (Render avtomatik topadi)

---

## 🗄️ 3-qadam: PostgreSQL Database yaratish

1. **Render Dashboard'da:**
   - **"New +"** tugmasini bosing
   - **"PostgreSQL"** ni tanlang

2. **Sozlamalar:**
   - **Name:** `pulsetrack-db`
   - **Database:** `pulsetrack`
   - **User:** `pulsetrack`
   - **Plan:** `Free`
   - **Region:** Eng yaqin region (masalan: Frankfurt)

3. **"Create Database"** tugmasini bosing

4. **Connection String'ni saqlang:**
   - Database yaratilgandan keyin
   - **"Info"** tab'da connection string ko'rinadi
   - Uni yozib oling (keyinroq kerak bo'ladi)

---

## 🚀 4-qadam: Web Service yaratish

### Variant A: render.yaml orqali (Avtomatik - Tavsiya etiladi)

1. **Dashboard'da:**
   - **"New +"** → **"Blueprint"**
   - Git reponizni tanlang
   - Render avtomatik `render.yaml` ni topadi

2. **"Apply"** tugmasini bosing
   - Render avtomatik database va web service yaratadi
   - Barcha environment variables sozlanadi

3. **Kutish:**
   - Build jarayoni 5-10 daqiqa davom etadi
   - Status "Live" bo'lguncha kuting

### Variant B: Qo'lda yaratish

1. **Dashboard'da:**
   - **"New +"** → **"Web Service"**
   - Git reponizni tanlang

2. **Basic Settings:**
   - **Name:** `pulsetrack-api`
   - **Environment:** `Node`
   - **Region:** Database bilan bir xil
   - **Branch:** `main` (yoki `master`)
   - **Root Directory:** `backend` (muhim!)
   - **Plan:** `Free`

3. **Build & Start:**
   - **Build Command:** `npm install && npm run build`
   - **Start Command:** `node dist/index.js`

4. **Environment Variables:**
   ```
   NODE_ENV=production
   PORT=4000
   DB_HOST=<database host (database Info'dan)>
   DB_PORT=5432
   DB_USER=pulsetrack
   DB_PASSWORD=<database password (database Info'dan)>
   DB_NAME=pulsetrack
   JWT_SECRET=<kuchli random key - openssl rand -base64 32>
   CORS_ORIGIN=*
   ```

5. **"Create Web Service"** tugmasini bosing

---

## ⏳ 5-qadam: Deploy jarayoni

1. **Build jarayoni:**
   - Render avtomatik `npm install` va `npm run build` ni ishga tushiradi
   - 5-10 daqiqa davom etadi
   - Log'larni kuzatib boring

2. **Xatoliklar bo'lsa:**
   - Log'larni tekshiring
   - Eng ko'p uchraydigan muammo: Root Directory noto'g'ri
   - Yechim: Root Directory = `backend`

3. **Muvaffaqiyatli deploy:**
   - Status "Live" bo'ladi
   - URL olinadi: `https://pulsetrack-api.onrender.com`

---

## ✅ 6-qadam: Tekshirish

### 1. Health Check:

```bash
# Browser'da yoki curl bilan:
https://pulsetrack-api.onrender.com/health

# Kutilgan javob:
{"status":"ok","version":"1.0.0"}
```

### 2. Login test:

```bash
curl -X POST https://pulsetrack-api.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@pulsetrack.com","password":"Admin123!"}'

# JWT token qaytishi kerak
```

---

## 📱 7-qadam: Flutter App yangilash

### APK ni yangi URL bilan qayta yig'ish:

```bash
cd whoop_app

# Render URL bilan
flutter build apk --release \
  --dart-define=API_BASE_URL=https://pulsetrack-api.onrender.com
```

### APK manzili:
```
C:\Users\User\Desktop\whoop\whoop_app\build\app\outputs\flutter-apk\app-release.apk
```

---

## ⚙️ 8-qadam: Sozlamalar (Ixtiyoriy)

### Render.com xususiyatlari:

1. **Auto-Deploy:**
   - Har safar Git'ga push qilsangiz, avtomatik redeploy bo'ladi
   - Settings → Auto-Deploy: Enabled

2. **Sleep Mode:**
   - 15 daqiqa ishlatilmasa, servis "uyquga" ketadi
   - Birinchi so'rov 30-60 soniya davom etadi
   - Yechim: UptimeRobot yoki boshqa monitoring (ixtiyoriy)

3. **Logs:**
   - Dashboard → Logs tab
   - Real-time log'larni ko'rish mumkin

4. **Metrics:**
   - CPU, Memory, Network usage
   - Free tier'da cheklangan

---

## 🔧 Muammolarni hal qilish

### Muammo 1: Build xatosi

**Xato:** `Cannot find module` yoki `npm install fails`

**Yechim:**
```bash
# Root Directory to'g'ri ekanligini tekshiring
# Root Directory = backend bo'lishi kerak

# Build Command:
npm install && npm run build

# Start Command:
node dist/index.js
```

### Muammo 2: Database ulanmayapti

**Xato:** `Failed to initialize data source`

**Yechim:**
1. Database Info'dan connection string'ni tekshiring
2. Environment variables to'g'ri ekanligini tekshiring:
   - `DB_HOST`
   - `DB_PORT`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`

### Muammo 3: Port xatosi

**Xato:** `Port already in use`

**Yechim:**
- Render avtomatik PORT environment variable beradi
- Kodda `process.env.PORT` ishlatilganligini tekshiring ✅ (allaqachon to'g'ri)

### Muammo 4: CORS xatosi

**Xato:** `CORS policy blocked`

**Yechim:**
- `CORS_ORIGIN=*` environment variable qo'shing
- Yoki aniq domain: `CORS_ORIGIN=https://yourdomain.com`

---

## 📊 Monitoring (Ixtiyoriy)

### UptimeRobot (Bepul)

1. **Ro'yxatdan o'ting:** https://uptimerobot.com
2. **New Monitor:**
   - Type: HTTP(s)
   - URL: `https://pulsetrack-api.onrender.com/health`
   - Interval: 5 minutes
3. **Natija:** Servis "uyqu"dan turganda avtomatik "uyg'onadi"

---

## ✅ Yakuniy tekshiruv

### Backend:
- [ ] Render.com'da service "Live" holatda
- [ ] Health check ishlayapti
- [ ] Database ulangan
- [ ] Login endpoint ishlayapti
- [ ] HTTPS ishlayapti (avtomatik)

### Frontend:
- [ ] APK yangi URL bilan yig'ilgan
- [ ] Telefonda o'rnatilgan
- [ ] API'ga ulanadi
- [ ] Barcha funksiyalar ishlayapti

---

## 🎯 Keyingi qadamlar

1. **Test qilish:**
   - Real bracelet bilan test qiling
   - Barcha funksiyalarni tekshiring
   - Metrikalarni yuborishni tekshiring

2. **Optimizatsiya:**
   - Log'larni tekshiring
   - Performance monitoring
   - Error tracking (Sentry - ixtiyoriy)

3. **Scaling:**
   - Agar trafik oshsa, paid plan'ga o'tish
   - Database backup sozlash
   - CDN qo'shish (ixtiyoriy)

---

## 📝 Muhim eslatmalar

1. **Free tier cheklovlari:**
   - Render: 750 soat/oy (yetarli MVP uchun)
   - Sleep mode: 15 daqiqadan keyin
   - Database: 1GB storage

2. **Xavfsizlik:**
   - JWT_SECRET kuchli bo'lishi kerak
   - .env fayllar Git'ga commit qilinmasligi kerak ✅
   - HTTPS avtomatik ishlayapti ✅

3. **Backup:**
   - Database backup sozlash (Render Pro'da avtomatik)
   - Yoki qo'lda: `pg_dump` orqali

---

## 🚀 Tez boshlash (5 daqiqa)

1. **GitHub'ga yuklang:**
   ```bash
   git add .
   git commit -m "Ready for Render"
   git push
   ```

2. **Render.com'da:**
   - New → Blueprint
   - Repo'ni tanlang
   - Apply

3. **Kuting:** 5-10 daqiqa

4. **URL oling:** `https://your-app.onrender.com`

5. **Flutter'ni yangilang:**
   ```bash
   flutter build apk --release \
     --dart-define=API_BASE_URL=https://your-app.onrender.com
   ```

**Tayyor! 🎉**

---

**Barcha kerakli fayllar tayyor! Endi Render.com'ga o'tib, deploy qilishingiz mumkin!**
