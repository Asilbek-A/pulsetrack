#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check backend status and test login API."""
import paramiko
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SERVER_IP = "155.212.219.232"
SERVER_USER = "root"
SERVER_PASS = "!vl10982dZm4"

def ssh_exec(ssh, cmd, desc=""):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    exit_status = stdout.channel.recv_exit_status()
    output = stdout.read().decode('utf-8', errors='replace').strip()
    if desc:
        print(f"  [{desc}]")
        if output:
            print(f"    {output[:500]}")
    return output, exit_status

print("=" * 50)
print("  CHECKING BACKEND STATUS")
print("=" * 50)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS, timeout=30,
                allow_agent=False, look_for_keys=False)
    print(f"\n[OK] Connected to {SERVER_IP}\n")

    # Check Node.js
    print("[1] Checking Node.js...")
    node_version, _ = ssh_exec(ssh, "node --version", "Node version")
    npm_version, _ = ssh_exec(ssh, "npm --version", "NPM version")

    # Check PM2
    print("\n[2] Checking PM2 processes...")
    pm2_list, _ = ssh_exec(ssh, "pm2 list", "PM2 processes")
    
    # Check backend directory
    print("\n[3] Checking backend directory...")
    backend_paths = [
        "/root/backend",
        "/var/www/backend",
        "/home/backend",
        "/opt/backend"
    ]
    
    backend_found = False
    for path in backend_paths:
        exists, _ = ssh_exec(ssh, f"test -d {path} && echo YES || echo NO", f"Checking {path}")
        if "YES" in exists:
            print(f"  [FOUND] Backend at: {path}")
            backend_found = True
            # Check if backend is running
            package_json, _ = ssh_exec(ssh, f"test -f {path}/package.json && echo YES || echo NO", "package.json")
            if "YES" in package_json:
                print(f"  [OK] package.json exists")
            break
    
    if not backend_found:
        print("  [WARNING] Backend directory not found in common locations")
        # Search for backend
        ssh_exec(ssh, "find / -name 'package.json' -type f 2>/dev/null | grep -E '(backend|api)' | head -5", "Searching for backend")

    # Check if backend port is listening
    print("\n[4] Checking backend port (4000)...")
    port_check, _ = ssh_exec(ssh, "netstat -tuln | grep :4000 || ss -tuln | grep :4000", "Port 4000")
    if ":4000" in port_check or "4000" in port_check:
        print("  [OK] Port 4000 is listening")
    else:
        print("  [WARNING] Port 4000 is NOT listening - backend may not be running")

    # Check Nginx proxy config
    print("\n[5] Checking Nginx API proxy...")
    nginx_config, _ = ssh_exec(ssh, "grep -A 5 'location /api' /etc/nginx/sites-available/default 2>/dev/null || echo 'No /api location found'", "Nginx /api config")
    
    # Check backend logs
    print("\n[6] Checking backend logs (PM2)...")
    pm2_logs, _ = ssh_exec(ssh, "pm2 logs --lines 20 --nostream 2>/dev/null || echo 'No PM2 logs'", "Recent PM2 logs")

    print("\n" + "=" * 50)
    print("  BACKEND CHECK COMPLETE")
    print("=" * 50)
    
    if ":4000" not in port_check:
        print("\n[!] Backend may not be running!")
        print("    Try: pm2 start <backend-path>/dist/index.js")
    else:
        print("\n[OK] Backend appears to be running on port 4000")
    
    print("=" * 50)

except Exception as e:
    print(f"\n[ERROR] {e}")
finally:
    ssh.close()
