# ⚡ Vercel - Flutter Web Deploy (Free & Stable)

## ✅ Nima uchun Vercel?

1. **100% Free** - Hech qanday to'lov yo'q
2. **Uyqu rejimi YO'Q** - 24/7 ishlaydi
3. **CDN** - Tez yuklanish
4. **SSL avtomatik** - HTTPS
5. **GitHub integration** - Avtomatik deploy
6. **Stabil** - Production-ready

## 📋 QADAM 1: Vercel'da Ro'yxatdan O'tish

1. https://vercel.com ga kiring
2. GitHub orqali ro'yxatdan o'ting
3. "Add New Project" bosing

## 🔧 QADAM 2: Flutter Web Build

```powershell
cd whoop_app
flutter build web --release --base-href / --web-renderer canvaskit
```

## 📦 QADAM 3: Vercel Deploy

### Variant A: GitHub Integration (Avtomatik)

1. Vercel Dashboard → "Add New Project"
2. GitHub repository tanlang: `Asilbek-A/pulsetrack`
3. **Root Directory**: `whoop_app`
4. **Build Command**: `flutter build web --release --base-href / --web-renderer canvaskit`
5. **Output Directory**: `build/web`
6. **Install Command**: `flutter pub get`
7. "Deploy" bosing

### Variant B: Vercel CLI (Manual)

```powershell
npm install -g vercel
cd whoop_app
vercel login
vercel --prod
```

## 🔗 QADAM 4: Custom Domain (Optional)

1. Vercel Dashboard → Project → Settings → Domains
2. Custom domain qo'shing
3. DNS sozlang

## ✅ TAYYOR!

Vercel avtomatik deploy qiladi va URL beradi:
- `https://pulsetrack.vercel.app`

---

## 📱 Mobile APK uchun:

Firebase App Distribution yoki direct APK download ishlatish mumkin.
