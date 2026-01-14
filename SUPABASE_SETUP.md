# 🚀 Supabase Database Setup - Free & Stable

## ✅ Nima uchun Supabase?

1. **100% Free Tier** - Cheksiz database
2. **Uyqu rejimi YO'Q** - 24/7 ishlaydi
3. **PostgreSQL** - Bizning TypeORM bilan mos
4. **Har bir foydalanuvchi uchun alohida database** - Multi-tenant support
5. **Stabil va ishonchli** - Production-ready

## 📋 QADAM 1: Supabase Project Yaratish

1. https://supabase.com ga kiring
2. "Start your project" bosing
3. GitHub orqali ro'yxatdan o'ting
4. "New Project" bosing
5. **Project Name**: `pulsetrack`
6. **Database Password**: Kuchli parol yarating (saqlang!)
7. **Region**: Eng yaqin region tanlang
8. "Create new project" bosing

## 🔑 QADAM 2: Database Connection String Olish

1. Project yaratilgandan keyin, **Settings** → **Database** ga kiring
2. **Connection string** ni ko'ring
3. **Connection pooling** ni tanlang (Session mode)
4. Connection string shunday ko'rinadi:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```

## 🔧 QADAM 3: Backend'ni Supabase'ga Ulash

Connection string'ni environment variable sifatida ishlatamiz.

## 📊 QADAM 4: Har Bir Foydalanuvchi Uchun Database

Supabase'da har bir foydalanuvchi uchun alohida schema yaratish mumkin:

```sql
-- Har bir foydalanuvchi uchun schema
CREATE SCHEMA IF NOT EXISTS user_123;
SET search_path TO user_123, public;
```

Yoki har bir foydalanuvchi uchun alohida database yaratish (Premium tier kerak).

**Free tier'da**: Bitta database, lekin har bir foydalanuvchi uchun alohida schema yoki table prefix ishlatish mumkin.

## ✅ TAYYOR!

Endi backend'ni Supabase'ga ulash kerak.
