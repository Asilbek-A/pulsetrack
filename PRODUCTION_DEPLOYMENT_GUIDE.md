# 🚀 Production Deployment Guide - PulseTrack

**Полное руководство по деплою в production**

---

## 📋 Чеклист перед началом

- [x] Код готов (критичные исправления применены)
- [x] APK собран с production URL
- [ ] VPS/сервер выбран и настроен
- [ ] Домен зарегистрирован (опционально, но рекомендуется)
- [ ] PostgreSQL база данных готова
- [ ] SSL сертификат получен

---

## 🖥️ Шаг 1: Выбор и настройка сервера

### Варианты серверов

**Рекомендуемые провайдеры:**
- **DigitalOcean** ($5-12/месяц) - простой, хорошая документация
- **Hetzner** (€4-10/месяц) - дешево, хорошая производительность
- **AWS EC2** ($10-20/месяц) - масштабируемо, много инструментов
- **Vultr** ($5-10/месяц) - хорошее соотношение цена/качество

### Минимальные требования

- **CPU:** 1-2 ядра
- **RAM:** 2GB (минимум), 4GB (рекомендуется)
- **Storage:** 20GB SSD
- **OS:** Ubuntu 22.04 LTS (рекомендуется)

### Настройка сервера

```bash
# 1. Подключиться к серверу
ssh root@your-server-ip

# 2. Обновить систему
apt update && apt upgrade -y

# 3. Установить необходимые пакеты
apt install -y curl wget git build-essential

# 4. Установить Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# 5. Проверить установку
node --version  # должно быть v20.x.x
npm --version

# 6. Установить PostgreSQL
apt install -y postgresql postgresql-contrib

# 7. Установить PM2 для управления процессом
npm install -g pm2

# 8. Настроить firewall
ufw allow 22/tcp    # SSH
ufw allow 80/tcp     # HTTP
ufw allow 443/tcp    # HTTPS
ufw enable
```

---

## 🗄️ Шаг 2: Настройка PostgreSQL

```bash
# 1. Переключиться на пользователя postgres
sudo -u postgres psql

# 2. Создать базу данных и пользователя
CREATE DATABASE pulsetrack_prod;
CREATE USER pulsetrack_user WITH ENCRYPTED PASSWORD 'your-strong-password-here';
GRANT ALL PRIVILEGES ON DATABASE pulsetrack_prod TO pulsetrack_user;
\q

# 3. Настроить PostgreSQL для удаленных подключений (если нужно)
# Отредактировать /etc/postgresql/14/main/postgresql.conf
# Раскомментировать: listen_addresses = 'localhost'

# Отредактировать /etc/postgresql/14/main/pg_hba.conf
# Добавить: host pulsetrack_prod pulsetrack_user 0.0.0.0/0 md5

# Перезапустить PostgreSQL
systemctl restart postgresql
```

---

## 📦 Шаг 3: Деплой Backend

### 3.1. Клонирование и настройка

```bash
# 1. Создать директорию для приложения
mkdir -p /var/www/pulsetrack
cd /var/www/pulsetrack

# 2. Клонировать репозиторий (или загрузить код)
git clone https://your-repo-url.git backend
# ИЛИ загрузить через scp/sftp

# 3. Перейти в директорию backend
cd backend

# 4. Установить зависимости
npm install

# 5. Создать .env файл из примера
cp env.example .env
nano .env  # или vim .env
```

### 3.2. Настройка .env для production

```env
# .env файл на сервере
NODE_ENV=production
PORT=4000

# Database (используйте данные из шага 2)
DB_HOST=localhost
DB_PORT=5432
DB_USER=pulsetrack_user
DB_PASSWORD=your-strong-password-here
DB_NAME=pulsetrack_prod

# JWT Secret (сгенерировать сильный ключ!)
# Используйте: openssl rand -base64 32
JWT_SECRET=your-very-strong-random-32-char-secret-key-here

# CORS (замените на ваш frontend домен)
CORS_ORIGIN=https://app.pulsetrack.com,https://pulsetrack.com
```

### 3.3. Сборка и запуск

```bash
# 1. Собрать TypeScript
npm run build

# 2. Проверить что dist/ директория создана
ls -la dist/

# 3. Запустить с PM2
pm2 start dist/index.js --name pulsetrack-api

# 4. Настроить автозапуск при перезагрузке
pm2 startup
pm2 save

# 5. Проверить статус
pm2 status
pm2 logs pulsetrack-api

# 6. Проверить что API работает
curl http://localhost:4000/health
```

---

## 🌐 Шаг 4: Настройка Nginx (Reverse Proxy)

### 4.1. Установка Nginx

```bash
apt install -y nginx
```

### 4.2. Настройка конфигурации

```bash
# Создать конфигурационный файл
nano /etc/nginx/sites-available/pulsetrack-api
```

**Содержимое файла:**
```nginx
server {
    listen 80;
    server_name api.pulsetrack.com;  # или ваш IP адрес

    location / {
        proxy_pass http://localhost:4000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 4.3. Активация конфигурации

```bash
# Создать символическую ссылку
ln -s /etc/nginx/sites-available/pulsetrack-api /etc/nginx/sites-enabled/

# Проверить конфигурацию
nginx -t

# Перезапустить Nginx
systemctl restart nginx

# Проверить статус
systemctl status nginx
```

---

## 🔒 Шаг 5: Настройка SSL/HTTPS (Let's Encrypt)

### 5.1. Установка Certbot

```bash
apt install -y certbot python3-certbot-nginx
```

### 5.2. Получение SSL сертификата

```bash
# Замените api.pulsetrack.com на ваш домен
certbot --nginx -d api.pulsetrack.com

# Следуйте инструкциям:
# - Введите email
# - Согласитесь с условиями
# - Certbot автоматически настроит Nginx
```

### 5.3. Автоматическое обновление

```bash
# Certbot автоматически настроит cron для обновления
# Проверить можно командой:
certbot renew --dry-run
```

---

## 📱 Шаг 6: Обновление Flutter App с Production URL

### 6.1. Обновить API URL в коде (если нужно)

Убедитесь что в `api_client.dart` используется правильный URL:

```dart
// При сборке APK используйте реальный production URL
flutter build apk --release \
  --dart-define=API_BASE_URL=https://api.pulsetrack.com
```

### 6.2. Собрать Production APK

```bash
cd whoop_app

# С production URL
flutter build apk --release \
  --dart-define=API_BASE_URL=https://api.pulsetrack.com

# APK будет в:
# build/app/outputs/flutter-apk/app-release.apk
```

### 6.3. Альтернатива: AAB для Google Play

```bash
# Если планируете публикацию в Google Play
flutter build appbundle --release \
  --dart-define=API_BASE_URL=https://api.pulsetrack.com

# AAB будет в:
# build/app/outputs/bundle/release/app-release.aab
```

---

## 🔍 Шаг 7: Проверка и тестирование

### 7.1. Проверка Backend

```bash
# 1. Health check
curl https://api.pulsetrack.com/health

# Ожидаемый ответ:
# {"status":"ok","version":"1.0.0"}

# 2. Проверить логи
pm2 logs pulsetrack-api

# 3. Проверить метрики PM2
pm2 monit
```

### 7.2. Тестирование API endpoints

```bash
# 1. Регистрация пользователя
curl -X POST https://api.pulsetrack.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# 2. Логин
curl -X POST https://api.pulsetrack.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@pulsetrack.com","password":"Admin123!"}'

# 3. Проверить метрики (с токеном)
curl -X GET https://api.pulsetrack.com/metrics \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 7.3. Тестирование Mobile App

1. Установить APK на телефон
2. Открыть приложение
3. Проверить подключение к API
4. Протестировать все функции:
   - Login/Register
   - BLE подключение
   - Отправка метрик
   - Получение данных

---

## 📊 Шаг 8: Мониторинг и логирование

### 8.1. PM2 Monitoring

```bash
# Установить PM2 monitoring
pm2 install pm2-logrotate

# Настроить ротацию логов
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7

# Просмотр логов
pm2 logs pulsetrack-api --lines 100
```

### 8.2. Настройка Uptime Monitoring (опционально)

**Рекомендуемые сервисы:**
- **UptimeRobot** (бесплатно, 50 мониторов)
- **Pingdom** (платно, но надежно)
- **StatusCake** (бесплатный план)

**Настройка:**
1. Зарегистрироваться на сервисе
2. Добавить монитор для `https://api.pulsetrack.com/health`
3. Настроить уведомления (email/SMS)

### 8.3. Database Backup

```bash
# Создать скрипт для бэкапа
nano /usr/local/bin/backup-pulsetrack-db.sh
```

**Содержимое:**
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/pulsetrack"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Создать бэкап
pg_dump -U pulsetrack_user pulsetrack_prod > $BACKUP_DIR/backup_$DATE.sql

# Удалить старые бэкапы (старше 7 дней)
find $BACKUP_DIR -name "backup_*.sql" -mtime +7 -delete

echo "Backup completed: backup_$DATE.sql"
```

```bash
# Сделать исполняемым
chmod +x /usr/local/bin/backup-pulsetrack-db.sh

# Добавить в cron (ежедневно в 2:00)
crontab -e
# Добавить строку:
0 2 * * * /usr/local/bin/backup-pulsetrack-db.sh
```

---

## 🔧 Шаг 9: Оптимизация и безопасность

### 9.1. Rate Limiting (рекомендуется)

```bash
# Установить express-rate-limit
cd /var/www/pulsetrack/backend
npm install express-rate-limit
```

**Добавить в `backend/src/index.ts`:**
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 минут
  max: 100, // максимум 100 запросов с одного IP
  message: 'Too many requests from this IP, please try again later.',
});

app.use('/api/', limiter);
```

### 9.2. Database Indexes

```sql
-- Подключиться к базе
sudo -u postgres psql pulsetrack_prod

-- Создать индексы для часто используемых полей
CREATE INDEX idx_health_metric_user_id ON health_metrics(user_id);
CREATE INDEX idx_health_metric_timestamp ON health_metrics(timestamp);
CREATE INDEX idx_user_email ON users(email);

\q
```

### 9.3. Обновление системы

```bash
# Настроить автоматические обновления безопасности
apt install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades
```

---

## 📝 Шаг 10: Документация и поддержка

### 10.1. Создать документацию API

Рекомендуется использовать Swagger/OpenAPI:

```bash
npm install swagger-ui-express swagger-jsdoc
```

### 10.2. Создать runbook для операций

Документировать:
- Как перезапустить сервис
- Как проверить логи
- Как сделать бэкап
- Как восстановить из бэкапа
- Контакты для экстренных случаев

---

## ✅ Финальный чеклист

### Backend
- [ ] Сервер настроен и обновлен
- [ ] Node.js установлен
- [ ] PostgreSQL установлен и настроен
- [ ] Backend код загружен на сервер
- [ ] `.env` файл создан с production значениями
- [ ] `npm run build` выполнен успешно
- [ ] PM2 запущен и настроен автозапуск
- [ ] Nginx настроен как reverse proxy
- [ ] SSL сертификат установлен
- [ ] API доступен по HTTPS
- [ ] Health check работает

### Frontend
- [ ] APK собран с production API URL
- [ ] APK протестирован на реальном устройстве
- [ ] Все функции работают
- [ ] Подключение к API работает

### Безопасность
- [ ] Firewall настроен
- [ ] SSL/HTTPS работает
- [ ] JWT_SECRET сильный и уникальный
- [ ] CORS настроен правильно
- [ ] Database пароль сильный
- [ ] `.env` файл защищен (не в git)

### Мониторинг
- [ ] PM2 monitoring настроен
- [ ] Логи ротируются
- [ ] Database backup настроен
- [ ] Uptime monitoring настроен (опционально)

---

## 🚨 Troubleshooting

### Проблема: API не отвечает

```bash
# Проверить статус PM2
pm2 status

# Проверить логи
pm2 logs pulsetrack-api

# Перезапустить
pm2 restart pulsetrack-api

# Проверить Nginx
systemctl status nginx
nginx -t
```

### Проблема: Database connection error

```bash
# Проверить что PostgreSQL запущен
systemctl status postgresql

# Проверить подключение
sudo -u postgres psql -d pulsetrack_prod

# Проверить .env файл
cat /var/www/pulsetrack/backend/.env | grep DB_
```

### Проблема: SSL не работает

```bash
# Проверить сертификат
certbot certificates

# Обновить вручную
certbot renew

# Проверить Nginx конфигурацию
nginx -t
systemctl reload nginx
```

---

## 📞 Поддержка

После деплоя рекомендуется:
1. Настроить мониторинг ошибок (Sentry, Rollbar)
2. Настроить алерты (email/SMS при проблемах)
3. Создать документацию для команды
4. Настроить CI/CD для автоматического деплоя (опционально)

---

## 🎯 Итоговая команда для быстрого деплоя

Если у вас уже есть настроенный сервер:

```bash
# На сервере
cd /var/www/pulsetrack/backend
git pull  # или загрузить новый код
npm install
npm run build
pm2 restart pulsetrack-api

# Проверить
curl https://api.pulsetrack.com/health
```

---

**Готово! Ваше приложение развернуто в production! 🚀**
