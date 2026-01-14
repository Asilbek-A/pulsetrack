# 🤖 Avtomatik Deploy Tizimi - To'liq Sozlash

## ✅ Bajarilgan ishlar:

1. ✅ GitHub Actions workflows yaratildi
2. ✅ Backend deploy workflow (Render.com)
3. ✅ Frontend deploy workflow (Vercel)
4. ✅ Database setup workflow (Supabase)

## 🔐 GitHub Secrets Sozlash

GitHub repository'da quyidagi secrets qo'shishingiz kerak:

### 1. GitHub Repository → Settings → Secrets and variables → Actions

### 2. Quyidagi Secrets qo'shing:

#### Backend (Render.com):
- `RENDER_SERVICE_ID` - Render.com service ID
- `RENDER_API_KEY` - Render.com API key

#### Frontend (Vercel):
- `VERCEL_TOKEN` - Vercel access token
- `VERCEL_ORG_ID` - Vercel organization ID
- `VERCEL_PROJECT_ID` - Vercel project ID
- `API_BASE_URL` - Backend API URL (masalan: `https://pulsetrack-api.onrender.com`)

#### Database (Supabase):
- `SUPABASE_DB_URL` - Supabase database connection string

## 📋 QADAM-BAQADAM SOZLASH:

### QADAM 1: Render.com API Key Olish

1. https://render.com ga kiring
2. Dashboard → Account Settings → API Keys
3. "Create API Key" bosing
4. Key nomi: `github-actions`
5. Key'ni ko'chirib oling

### QADAM 2: Vercel Token Olish

1. https://vercel.com ga kiring
2. Account Settings → Tokens
3. "Create Token" bosing
4. Token nomi: `github-actions`
5. Scope: Full Account
6. Token'ni ko'chirib oling

### QADAM 3: Vercel Project ID va Org ID

1. Vercel Dashboard → Project → Settings
2. **Project ID** va **Team ID** (Org ID) ni ko'ring

### QADAM 4: Supabase Connection String

1. Supabase Dashboard → Settings → Database
2. Connection string'ni ko'ring
3. Connection pooling (Session mode) tanlang

### QADAM 5: GitHub Secrets Qo'shish

1. https://github.com/Asilbek-A/pulsetrack → Settings
2. Secrets and variables → Actions
3. "New repository secret" bosing
4. Har bir secret'ni qo'shing:

```
RENDER_SERVICE_ID = [Render service ID]
RENDER_API_KEY = [Render API key]
VERCEL_TOKEN = [Vercel token]
VERCEL_ORG_ID = [Vercel org ID]
VERCEL_PROJECT_ID = [Vercel project ID]
API_BASE_URL = https://pulsetrack-api.onrender.com
SUPABASE_DB_URL = postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres
```

## 🚀 AVTOMATIK DEPLOY

Barcha secrets sozlangandan keyin:

1. **Backend o'zgarganda** → Avtomatik Render.com'ga deploy qilinadi
2. **Frontend o'zgarganda** → Avtomatik Vercel'ga deploy qilinadi
3. **Database o'zgarganda** → Avtomatik Supabase'ga sozlanadi

## ✅ TAYYOR!

Endi har safar GitHub'ga push qilsangiz, avtomatik deploy qilinadi!
