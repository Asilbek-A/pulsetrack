# 🌐 Netlify - Flutter Web Deploy (Free & Stable)

## ✅ Nima uchun Netlify?

1. **100% Free** - Hech qanday to'lov yo'q
2. **Uyqu rejimi YO'Q** - 24/7 ishlaydi
3. **CDN** - Tez yuklanish
4. **SSL avtomatik** - HTTPS
5. **GitHub integration** - Avtomatik deploy
6. **Stabil** - Production-ready

## 📋 QADAM 1: Netlify'da Ro'yxatdan O'tish

1. https://netlify.com ga kiring
2. GitHub orqali ro'yxatdan o'ting
3. "Add new site" → "Import an existing project"

## 🔧 QADAM 2: Flutter Web Build

```powershell
cd whoop_app
flutter build web --release --base-href / --web-renderer canvaskit
```

## 📦 QADAM 3: Netlify Deploy

### Variant A: GitHub Integration (Avtomatik)

1. Netlify Dashboard → "Add new site" → "Import an existing project"
2. GitHub repository tanlang: `Asilbek-A/pulsetrack`
3. **Base directory**: `whoop_app`
4. **Build command**: `flutter build web --release --base-href / --web-renderer canvaskit`
5. **Publish directory**: `whoop_app/build/web`
6. "Deploy site" bosing

### Variant B: Netlify CLI (Manual)

```powershell
npm install -g netlify-cli
cd whoop_app
netlify login
netlify deploy --prod --dir=build/web
```

## 🔗 QADAM 4: Custom Domain (Optional)

1. Netlify Dashboard → Site settings → Domain management
2. Custom domain qo'shing
3. DNS sozlang

## ✅ TAYYOR!

Netlify avtomatik deploy qiladi va URL beradi:
- `https://pulsetrack.netlify.app`

---

## 📱 Mobile APK uchun:

Firebase App Distribution yoki direct APK download ishlatish mumkin.
