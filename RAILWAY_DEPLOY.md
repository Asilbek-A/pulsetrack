# 🚂 Railway.app - Free Alternative (Stable, No Sleep)

## ✅ Nima uchun Railway.app?

1. **$5/oy** - Juda arzon (free tier yo'q, lekin arzon)
2. **Uyqu rejimi YO'Q** - 24/7 ishlaydi
3. **PostgreSQL database** - Bepul (500MB)
4. **Stabil va ishonchli** - Production-ready
5. **Avtomatik deploy** - GitHub'dan avtomatik

## 📋 QADAM 1: Railway.app'da Ro'yxatdan O'tish

1. https://railway.app ga kiring
2. GitHub orqali ro'yxatdan o'ting
3. "New Project" bosing
4. "Deploy from GitHub repo" tanlang
5. Repository tanlang: `Asilbek-A/pulsetrack`

## 🗄️ QADAM 2: PostgreSQL Database Yaratish

1. Project ichida "New" → "Database" → "PostgreSQL"
2. Database avtomatik yaratiladi
3. **Variables** tab'da connection string ko'rinadi

## 🔧 QADAM 3: Environment Variables

Railway avtomatik database connection string'ni `DATABASE_URL` sifatida beradi.

Backend'da `DATABASE_URL` ni parse qilish kerak yoki alohida variables qo'shish:

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

## ✅ TAYYOR!

Railway.app $5/oy, lekin:
- ✅ Uyqu rejimi yo'q
- ✅ Stabil
- ✅ Database bepul (500MB)
- ✅ Avtomatik deploy
