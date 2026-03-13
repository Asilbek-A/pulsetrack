# Manual Deployment Guide

## Option 1: Using WinSCP (Recommended for Windows)

1. Download WinSCP: https://winscp.net/
2. Connect to server:
   - Host: `185.71.76.0`
   - Username: `u2064500`
   - Password: `pulsetrack2024`
   - Port: `22`

3. Navigate to: `/var/www/pulsetrack/data/www/pulsetrack.com`

4. Delete all files in that directory

5. Upload all files from: `C:\Users\User\Desktop\whoop\whoop_app\build\web\`

6. Make sure `index.html` is in the root

## Option 2: Using PowerShell SCP

```powershell
cd C:\Users\User\Desktop\whoop\whoop_app\build\web

# Create a tar archive (if tar is available)
# Or use pscp (PuTTY SCP) if installed

# Using pscp (download from PuTTY):
pscp -r * u2064500@185.71.76.0:/var/www/pulsetrack/data/www/pulsetrack.com/
```

## Option 3: Using Git (if server has git)

If the server has git access, you can:
1. Commit and push to GitHub (already done)
2. SSH to server and pull:
   ```bash
   cd /var/www/pulsetrack/data/www/pulsetrack.com
   git pull origin main
   ```

## Option 4: Fix SSH Connection

The Python script is failing due to SSH connection issues. Try:
- Check if SSH port 22 is open
- Try connecting manually first: `ssh u2064500@185.71.76.0`
- Check server firewall settings
- Try different SSH port if configured

## Files to Upload

All files from: `whoop_app\build\web\`
- index.html
- main.dart.js
- assets/ (entire folder)
- flutter.js
- etc.
