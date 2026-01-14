# 🔐 GitHub'ga Login va Repository Yaratish

## ✅ QADAM 1: GitHub'da ro'yxatdan o'tish (agar akkaunt yo'q bo'lsa)

1. https://github.com ga kiring
2. "Sign up" tugmasini bosing
3. Email, parol va username kiriting
4. Email'ni tasdiqlang

## 🔑 QADAM 2: GitHub'ga Login qilish

### Variant A: GitHub.com orqali (Web)

1. https://github.com ga kiring
2. "Sign in" tugmasini bosing
3. **Username yoki Email** kiriting
4. **Parol** kiriting
5. "Sign in" bosing

### Variant B: Git orqali kod yuklash (Terminal)

GitHub endi **parol** qabul qilmaydi. **Personal Access Token (PAT)** kerak:

#### 2.1. Personal Access Token yaratish:

1. GitHub'ga login qiling
2. O'ng yuqori burchakda **profil rasmingiz** → **Settings**
3. Pastga scroll qiling → **Developer settings**
4. **Personal access tokens** → **Tokens (classic)**
5. **Generate new token** → **Generate new token (classic)**
6. **Note**: `PulseTrack Deployment` (yoki istalgan nom)
7. **Expiration**: 90 days (yoki istalgan muddat)
8. **Scopes** (permissions):
   - ✅ **repo** (Full control of private repositories)
   - ✅ **workflow** (Update GitHub Action workflows)
9. **Generate token** bosing
10. **TOKEN'ni ko'chirib oling!** (keyin ko'rinmaydi!)

#### 2.2. Token'ni ishlatish:

```powershell
# Git push qilganda:
git push -u origin main

# Username so'ralganda: GitHub username'ingizni kiriting
# Password so'ralganda: Token'ni kiriting (parol emas!)
```

## 📦 QADAM 3: Repository yaratish

1. GitHub'ga login qiling
2. O'ng yuqori burchakda **"+"** → **"New repository"**
3. **Repository name**: `pulsetrack`
4. **Description**: "WHOOP-style fitness tracking app" (ixtiyoriy)
5. **Public** qiling (Render.com bepul tier uchun kerak)
6. **"Initialize with README"** ni **O'CHIRING** (bizda allaqachon kod bor)
7. **"Create repository"** bosing

## 🚀 QADAM 4: Kod yuklash

### 4.1. Remote qo'shish:

```powershell
# YOUR_USERNAME o'rniga GitHub username'ingizni qo'ying
git remote add origin https://github.com/YOUR_USERNAME/pulsetrack.git
```

**Misol:**
```powershell
git remote add origin https://github.com/johndoe/pulsetrack.git
```

### 4.2. Branch nomini o'zgartirish:

```powershell
git branch -M main
```

### 4.3. Kod yuklash:

```powershell
git push -u origin main
```

**Login so'ralganda:**
- **Username**: GitHub username'ingiz
- **Password**: Personal Access Token (parol emas!)

## 🔄 QADAM 5: Keyingi marta (token saqlangan bo'lsa)

Agar Git Credential Manager token'ni saqlagan bo'lsa, keyingi safar avtomatik ishlaydi.

## ⚠️ MUHIM ESLATMALAR:

1. **Parol ishlamaydi!** - Faqat Personal Access Token ishlaydi
2. **Token'ni saqlang!** - Keyin ko'rinmaydi, qayta yaratish kerak bo'ladi
3. **Token xavfsizligi**: Hech kimga bermang, parol kabi saqlang

## 🆘 Muammo bo'lsa:

### "Authentication failed" xatosi:

1. Token'ni tekshiring (to'g'ri ko'chirilganmi?)
2. Token muddati tugagan bo'lishi mumkin (yangi yarating)
3. `repo` scope tanlanganligini tekshiring

### "Repository not found" xatosi:

1. Repository nomini tekshiring
2. Repository Public yoki sizga access borligini tekshiring
3. Remote URL'ni tekshiring: `git remote -v`

---

## 📝 QISQA YO'RIQNOMA:

1. GitHub.com → Login (username + parol)
2. Settings → Developer settings → Personal access tokens → Generate
3. Token'ni ko'chirib oling
4. Repository yarating
5. `git remote add origin https://github.com/USERNAME/pulsetrack.git`
6. `git push -u origin main` (username + token)
