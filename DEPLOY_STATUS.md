# 📊 DEPLOY HOLATI

## ✅ TAYYORLANGAN:

### 1. GitHub Actions Workflows
- ✅ `deploy-backend.yml` - Backend Render.com'ga deploy
- ✅ `deploy-frontend-vercel.yml` - Frontend Vercel'ga deploy
- ✅ `setup-database.yml` - Database Supabase sozlash
- ✅ `full-deploy.yml` - To'liq deploy (barcha servislar)

### 2. Konfiguratsiyalar
- ✅ `render.yaml` - Render.com backend konfiguratsiyasi
- ✅ `whoop_app/vercel.json` - Vercel frontend konfiguratsiyasi
- ✅ `backend/src/infra/data-source.ts` - Database connection (SSL support)

### 3. Qo'llanmalar
- ✅ `AUTOMATIC_DEPLOY_SETUP.md` - To'liq sozlash
- ✅ `DEPLOY_NOW.md` - Deploy qilish qo'llanmasi
- ✅ `SETUP_COMPLETE.md` - Checklist

## 🔄 DEPLOY QILISH:

### GitHub Actions orqali:

1. https://github.com/Asilbek-A/pulsetrack → Actions
2. "Full Deployment" workflow'ni tanlang
3. "Run workflow" bosing
4. Deploy qilish kerak bo'lgan servislarni belgilang
5. "Run workflow" bosing

## ⚠️ KERAKLI: GitHub Secrets

Workflow'lar ishlashi uchun secrets qo'shishingiz kerak:

- `RENDER_SERVICE_ID`
- `RENDER_API_KEY`
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`
- `API_BASE_URL`
- `SUPABASE_DB_URL`

## 📋 KEYINGI QADAM:

1. GitHub Secrets qo'shish
2. GitHub Actions orqali deploy qilish
3. Yoki birinchi marta manual deploy qilish

## ✅ TAYYOR!

Barcha tayyorlovlar tugallandi. Endi deploy qilishingiz mumkin!
