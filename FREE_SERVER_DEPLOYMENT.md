# 🆓 Бесплатный Production Деплой - PulseTrack

**Профессиональная установка на бесплатные платформы**

---

## 🎯 Выбор бесплатной платформы

### Рекомендуемые варианты:

1. **Render.com** ⭐ (Лучший выбор)
   - ✅ Бесплатный PostgreSQL
   - ✅ Бесплатный Web Service
   - ✅ Автоматический SSL
   - ✅ Простой деплой из Git
   - ⚠️ Ограничение: сервис засыпает после 15 минут бездействия

2. **Railway.app**
   - ✅ Бесплатный tier ($5 кредитов/месяц)
   - ✅ PostgreSQL включен
   - ✅ Автоматический деплой
   - ⚠️ Ограниченный трафик

3. **Fly.io**
   - ✅ Бесплатный tier
   - ✅ PostgreSQL доступен
   - ⚠️ Более сложная настройка

**Рекомендация: Render.com** - самый простой и надежный для MVP.

---

## 🚀 Вариант 1: Render.com (Рекомендуется)

### Шаг 1: Подготовка репозитория

```bash
# Убедитесь что код в Git репозитории
cd C:\Users\User\Desktop\whoop
git init  # если еще не инициализирован
git add .
git commit -m "Initial commit for deployment"
```

### Шаг 2: Создать render.yaml для автоматической настройки

Создайте файл `render.yaml` в корне проекта:

```yaml
services:
  - type: web
    name: pulsetrack-api
    env: node
    plan: free
    buildCommand: cd backend && npm install && npm run build
    startCommand: cd backend && node dist/index.js
    envVars:
      - key: NODE_ENV
        value: production
      - key: PORT
        value: 4000
      - key: DB_HOST
        fromDatabase:
          name: pulsetrack-db
          property: host
      - key: DB_PORT
        fromDatabase:
          name: pulsetrack-db
          property: port
      - key: DB_USER
        fromDatabase:
          name: pulsetrack-db
          property: user
      - key: DB_PASSWORD
        fromDatabase:
          name: pulsetrack-db
          property: password
      - key: DB_NAME
        fromDatabase:
          name: pulsetrack-db
          property: database
      - key: JWT_SECRET
        generateValue: true
      - key: CORS_ORIGIN
        value: "*"

databases:
  - name: pulsetrack-db
    plan: free
    databaseName: pulsetrack
    user: pulsetrack
```

### Шаг 3: Создать необходимые файлы для Render

#### 3.1. Создать `backend/render-build.sh`

```bash
#!/bin/bash
set -e
cd backend
npm install
npm run build
```

#### 3.2. Обновить `backend/package.json` для production

Убедитесь что есть скрипт `start`:

```json
{
  "scripts": {
    "dev": "ts-node-dev --respawn --transpile-only src/index.ts",
    "build": "tsc -p tsconfig.json",
    "start": "node dist/index.js"
  }
}
```

### Шаг 4: Деплой на Render.com

1. **Зарегистрироваться:**
   - Перейти на https://render.com
   - Sign up с GitHub/GitLab/Bitbucket

2. **Подключить репозиторий:**
   - Dashboard → New → Blueprint
   - Подключить ваш Git репозиторий
   - Render автоматически обнаружит `render.yaml`

3. **Или создать вручную:**

   **a) Создать PostgreSQL Database:**
   - Dashboard → New → PostgreSQL
   - Name: `pulsetrack-db`
   - Plan: Free
   - Database: `pulsetrack`
   - User: `pulsetrack`
   - Нажать "Create Database"
   - Сохранить connection string

   **b) Создать Web Service:**
   - Dashboard → New → Web Service
   - Connect ваш репозиторий
   - Settings:
     - Name: `pulsetrack-api`
     - Environment: `Node`
     - Build Command: `cd backend && npm install && npm run build`
     - Start Command: `cd backend && node dist/index.js`
     - Plan: Free

   **c) Настроить Environment Variables:**
   ```
   NODE_ENV=production
   PORT=4000
   DB_HOST=<из database connection string>
   DB_PORT=5432
   DB_USER=<из database connection string>
   DB_PASSWORD=<из database connection string>
   DB_NAME=pulsetrack
   JWT_SECRET=<сгенерировать сильный ключ>
   CORS_ORIGIN=*
   ```

4. **Деплой:**
   - Нажать "Create Web Service"
   - Render автоматически соберет и запустит
   - Дождаться завершения (5-10 минут)

5. **Получить URL:**
   - После деплоя получите URL типа: `https://pulsetrack-api.onrender.com`
   - Это ваш production API URL!

### Шаг 5: Обновить Flutter App

```bash
cd whoop_app

# Собрать APK с Render URL
flutter build apk --release \
  --dart-define=API_BASE_URL=https://pulsetrack-api.onrender.com
```

---

## 🚂 Вариант 2: Railway.app

### Шаг 1: Подготовка

1. Зарегистрироваться на https://railway.app
2. Создать новый проект
3. Подключить Git репозиторий

### Шаг 2: Добавить PostgreSQL

1. В проекте нажать "New"
2. Выбрать "Database" → "PostgreSQL"
3. Railway автоматически создаст базу

### Шаг 3: Добавить Web Service

1. В проекте нажать "New" → "GitHub Repo"
2. Выбрать ваш репозиторий
3. Railway автоматически определит Node.js

### Шаг 4: Настроить переменные окружения

Railway автоматически создаст переменные для базы данных. Добавить вручную:

```
NODE_ENV=production
JWT_SECRET=<сгенерировать>
CORS_ORIGIN=*
```

### Шаг 5: Настроить деплой

1. Settings → Deploy
2. Root Directory: `backend`
3. Build Command: `npm install && npm run build`
4. Start Command: `node dist/index.js`

### Шаг 6: Получить URL

Railway даст URL типа: `https://pulsetrack-production.up.railway.app`

---

## 🪶 Вариант 3: Fly.io

### Шаг 1: Установка Fly CLI

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex
```

### Шаг 2: Логин

```bash
fly auth login
```

### Шаг 3: Создать приложение

```bash
cd backend
fly launch
# Следовать инструкциям
```

### Шаг 4: Настроить PostgreSQL

```bash
fly postgres create --name pulsetrack-db
fly postgres attach pulsetrack-db
```

### Шаг 5: Настроить переменные

```bash
fly secrets set JWT_SECRET=your-secret-key
fly secrets set NODE_ENV=production
```

### Шаг 6: Деплой

```bash
fly deploy
```

---

## 📝 Создание необходимых файлов

### 1. render.yaml (для Render.com)

Создайте в корне проекта:

```yaml
services:
  - type: web
    name: pulsetrack-api
    env: node
    plan: free
    buildCommand: cd backend && npm install && npm run build
    startCommand: cd backend && node dist/index.js
    envVars:
      - key: NODE_ENV
        value: production
      - key: PORT
        value: 4000
      - key: DB_HOST
        fromDatabase:
          name: pulsetrack-db
          property: host
      - key: DB_PORT
        fromDatabase:
          name: pulsetrack-db
          property: port
      - key: DB_USER
        fromDatabase:
          name: pulsetrack-db
          property: user
      - key: DB_PASSWORD
        fromDatabase:
          name: pulsetrack-db
          property: password
      - key: DB_NAME
        fromDatabase:
          name: pulsetrack-db
          property: database
      - key: JWT_SECRET
        generateValue: true
      - key: CORS_ORIGIN
        value: "*"

databases:
  - name: pulsetrack-db
    plan: free
    databaseName: pulsetrack
    user: pulsetrack
```

### 2. Обновить backend/src/index.ts для Render

Убедитесь что сервер слушает правильный порт:

```typescript
const PORT = process.env.PORT || 4000;
app.listen(Number(PORT), '0.0.0.0', () => {
  console.log(`API server listening on http://0.0.0.0:${PORT}`);
});
```

### 3. Создать Procfile (опционально, для некоторых платформ)

```
web: cd backend && node dist/index.js
```

---

## 🔧 Настройка для бесплатного tier

### Render.com особенности:

1. **Sleep Mode:** Сервис засыпает после 15 минут бездействия
   - Первый запрос после пробуждения займет 30-60 секунд
   - Решение: Использовать uptime monitoring (UptimeRobot) для "разбудить" сервис

2. **Ограничения:**
   - 750 часов/месяц бесплатно
   - Достаточно для MVP/тестирования

### Оптимизация для бесплатного tier:

1. **Минимизировать зависимости:**
   ```bash
   # Удалить devDependencies из production
   npm install --production
   ```

2. **Оптимизировать build:**
   - Убедиться что `dist/` не содержит лишних файлов
   - Использовать `.dockerignore` если используете Docker

---

## ✅ Чеклист деплоя

### Подготовка:
- [ ] Код в Git репозитории
- [ ] `render.yaml` создан (для Render)
- [ ] `package.json` имеет скрипт `start`
- [ ] Backend компилируется (`npm run build`)

### Деплой:
- [ ] Зарегистрирован на платформе
- [ ] Репозиторий подключен
- [ ] Database создана
- [ ] Web Service создан
- [ ] Environment variables настроены
- [ ] Деплой завершен успешно
- [ ] Health check работает: `curl https://your-app.onrender.com/health`

### Тестирование:
- [ ] API доступен по HTTPS
- [ ] `/health` endpoint отвечает
- [ ] `/auth/login` работает
- [ ] Database подключение работает
- [ ] Flutter app подключается к API

---

## 🚀 Быстрый старт (Render.com)

### Минимальные шаги:

1. **Создать аккаунт:** https://render.com → Sign up

2. **Создать Database:**
   - New → PostgreSQL
   - Name: `pulsetrack-db`
   - Plan: Free
   - Create

3. **Создать Web Service:**
   - New → Web Service
   - Connect ваш Git repo
   - Settings:
     - Build: `cd backend && npm install && npm run build`
     - Start: `cd backend && node dist/index.js`
   - Add Environment Variables:
     ```
     NODE_ENV=production
     PORT=4000
     DB_HOST=<из database>
     DB_PORT=5432
     DB_USER=<из database>
     DB_PASSWORD=<из database>
     DB_NAME=pulsetrack
     JWT_SECRET=<сгенерировать>
     CORS_ORIGIN=*
     ```
   - Create Web Service

4. **Дождаться деплоя** (5-10 минут)

5. **Получить URL:** `https://your-app.onrender.com`

6. **Обновить Flutter:**
   ```bash
   flutter build apk --release \
     --dart-define=API_BASE_URL=https://your-app.onrender.com
   ```

---

## 🔍 Проверка после деплоя

```bash
# 1. Health check
curl https://your-app.onrender.com/health

# Ожидаемый ответ:
# {"status":"ok","version":"1.0.0"}

# 2. Test login
curl -X POST https://your-app.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@pulsetrack.com","password":"Admin123!"}'

# Должен вернуть JWT token
```

---

## 📱 Обновление Flutter App

После получения production URL:

```bash
cd whoop_app

# Собрать с production URL
flutter build apk --release \
  --dart-define=API_BASE_URL=https://your-app.onrender.com

# APK готов:
# build/app/outputs/flutter-apk/app-release.apk
```

---

## ⚠️ Важные замечания

1. **Render.com Sleep Mode:**
   - Первый запрос после пробуждения медленный
   - Используйте UptimeRobot для поддержания активности (опционально)

2. **Бесплатные ограничения:**
   - Render: 750 часов/месяц
   - Railway: $5 кредитов/месяц
   - Fly.io: ограниченный трафик

3. **Безопасность:**
   - JWT_SECRET должен быть сильным
   - Не коммитьте `.env` файлы
   - Используйте HTTPS (автоматически на Render/Railway)

---

## 🎯 Рекомендация

**Для MVP/тестирования:** Render.com - самый простой вариант
- Автоматический SSL
- Простая настройка
- Бесплатный PostgreSQL
- Автоматический деплой из Git

**Следующие шаги:**
1. Зарегистрироваться на Render.com
2. Создать database и web service
3. Дождаться деплоя
4. Обновить Flutter app с новым URL
5. Протестировать!

---

**Готово к деплою! 🚀**
