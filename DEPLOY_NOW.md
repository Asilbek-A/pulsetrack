# 🚀 DEPLOY QILISH - HOZIR

## ✅ Barcha tayyorlovlar tugallandi!

GitHub Actions workflows yaratildi va GitHub'ga yuklandi.

## 🔄 AVTOMATIK DEPLOY

### Variant 1: GitHub Actions orqali (Tavsiya)

1. **GitHub Repository'ga kiring**: https://github.com/Asilbek-A/pulsetrack
2. **Actions** tab'ga o'ting
3. **"Full Deployment"** workflow'ni tanlang
4. **"Run workflow"** bosing
5. Quyidagilarni belgilang:
   - ✅ Deploy Backend to Render
   - ✅ Deploy Frontend to Vercel
   - ✅ Setup Database (Supabase)
6. **"Run workflow"** bosing

### Variant 2: Har birini alohida

**Backend deploy:**
- Actions → "Deploy Backend to Render" → Run workflow

**Frontend deploy:**
- Actions → "Deploy Frontend to Vercel" → Run workflow

**Database setup:**
- Actions → "Setup Supabase Database" → Run workflow

## ⚠️ MUHIM: GitHub Secrets

Workflow'lar ishlashi uchun GitHub Secrets qo'shishingiz kerak:

1. Repository → Settings → Secrets and variables → Actions
2. Quyidagi secrets qo'shing:

```
RENDER_SERVICE_ID = [Render service ID]
RENDER_API_KEY = [Render API key]
VERCEL_TOKEN = [Vercel token]
VERCEL_ORG_ID = [Vercel org ID]
VERCEL_PROJECT_ID = [Vercel project ID]
API_BASE_URL = https://pulsetrack-api.onrender.com
SUPABASE_DB_URL = [Supabase connection string]
```

## 📋 BIRINCHI MARTA DEPLOY (Manual)

Agar secrets hali sozlanmagan bo'lsa, birinchi marta manual deploy qilish kerak:

### Backend (Render.com):

1. https://render.com → New → Blueprint
2. Repository: `Asilbek-A/pulsetrack`
3. Deploy qiling
4. Service ID ni oling → GitHub Secrets ga qo'shing

### Frontend (Vercel):

1. https://vercel.com → Add New Project
2. Repository: `Asilbek-A/pulsetrack`
3. Root Directory: `whoop_app`
4. Deploy qiling
5. Project ID va Org ID ni oling → GitHub Secrets ga qo'shing

### Database (Supabase):

1. https://supabase.com → New Project
2. Project yarating
3. Connection string ni oling → GitHub Secrets ga qo'shing

## ✅ TAYYOR!

Barcha workflows tayyor. Endi GitHub Actions orqali deploy qilishingiz mumkin!
