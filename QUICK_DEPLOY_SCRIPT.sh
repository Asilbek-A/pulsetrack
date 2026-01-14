#!/bin/bash
# Quick Deployment Script for PulseTrack Backend
# Usage: ./quick_deploy.sh

set -e  # Exit on error

echo "🚀 PulseTrack Backend Deployment Script"
echo "========================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root or with sudo${NC}"
    exit 1
fi

# Step 1: Update system
echo -e "${YELLOW}[1/8] Updating system...${NC}"
apt update && apt upgrade -y

# Step 2: Install Node.js
echo -e "${YELLOW}[2/8] Installing Node.js...${NC}"
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt install -y nodejs
fi
echo -e "${GREEN}Node.js version: $(node --version)${NC}"

# Step 3: Install PostgreSQL
echo -e "${YELLOW}[3/8] Installing PostgreSQL...${NC}"
if ! command -v psql &> /dev/null; then
    apt install -y postgresql postgresql-contrib
    systemctl start postgresql
    systemctl enable postgresql
fi

# Step 4: Install PM2
echo -e "${YELLOW}[4/8] Installing PM2...${NC}"
if ! command -v pm2 &> /dev/null; then
    npm install -g pm2
fi

# Step 5: Install Nginx
echo -e "${YELLOW}[5/8] Installing Nginx...${NC}"
if ! command -v nginx &> /dev/null; then
    apt install -y nginx
    systemctl start nginx
    systemctl enable nginx
fi

# Step 6: Setup firewall
echo -e "${YELLOW}[6/8] Configuring firewall...${NC}"
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# Step 7: Create application directory
echo -e "${YELLOW}[7/8] Setting up application directory...${NC}"
APP_DIR="/var/www/pulsetrack"
mkdir -p $APP_DIR
cd $APP_DIR

echo -e "${GREEN}Application directory: $APP_DIR${NC}"
echo -e "${YELLOW}Please:${NC}"
echo "  1. Upload backend code to $APP_DIR/backend"
echo "  2. Create .env file from env.example"
echo "  3. Run: cd $APP_DIR/backend && npm install && npm run build"
echo "  4. Run: pm2 start dist/index.js --name pulsetrack-api"
echo "  5. Run: pm2 startup && pm2 save"

# Step 8: Install Certbot (optional)
echo -e "${YELLOW}[8/8] Installing Certbot (for SSL)...${NC}"
if ! command -v certbot &> /dev/null; then
    apt install -y certbot python3-certbot-nginx
    echo -e "${GREEN}Certbot installed. Run: certbot --nginx -d your-domain.com${NC}"
fi

echo ""
echo -e "${GREEN}✅ Basic setup completed!${NC}"
echo ""
echo "Next steps:"
echo "1. Upload backend code"
echo "2. Configure .env file"
echo "3. Build and start application"
echo "4. Configure Nginx"
echo "5. Setup SSL certificate"
