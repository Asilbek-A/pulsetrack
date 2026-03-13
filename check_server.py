#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check server setup and configure if needed."""
import paramiko
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SERVER_IP = "155.212.219.232"
SERVER_USER = "root"
SERVER_PASS = "!vl10982dZm4"
WEB_PATH = "/var/www/html"

def ssh_exec(ssh, cmd, desc=""):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    exit_status = stdout.channel.recv_exit_status()
    output = stdout.read().decode('utf-8', errors='replace').strip()
    if desc:
        print(f"  [{desc}]")
        if output:
            print(f"    {output[:300]}")
    return output

print("=" * 50)
print("  CHECKING SERVER SETUP")
print("=" * 50)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS, timeout=30,
                allow_agent=False, look_for_keys=False)
    print(f"\n[OK] Connected to {SERVER_IP}\n")

    # Check web server
    print("[1] Checking web server...")
    ssh_exec(ssh, "which nginx", "Nginx")
    ssh_exec(ssh, "which apache2", "Apache")
    ssh_exec(ssh, "systemctl is-active nginx 2>/dev/null || systemctl is-active apache2 2>/dev/null || echo 'No web server active'", "Web server status")

    # Check web files
    print("\n[2] Checking web files...")
    ssh_exec(ssh, f"ls -la {WEB_PATH} | head -10", "Web directory contents")
    ssh_exec(ssh, f"test -f {WEB_PATH}/index.html && echo 'index.html exists' || echo 'index.html NOT FOUND'", "index.html")

    # Check nginx config
    print("\n[3] Checking Nginx configuration...")
    nginx_config = ssh_exec(ssh, "cat /etc/nginx/sites-available/default 2>/dev/null | head -30", "Default nginx config")
    
    if "try_files" not in nginx_config:
        print("\n[!] Nginx may need configuration for SPA routing")
        print("    Need to add 'try_files $uri $uri/ /index.html;' to location /")
    
    # Test nginx config
    ssh_exec(ssh, "nginx -t 2>&1", "Nginx config test")

    print("\n" + "=" * 50)
    print("  SERVER CHECK COMPLETE")
    print("=" * 50)
    print(f"\n  Web app should be at: http://{SERVER_IP}/")
    print("=" * 50)

except Exception as e:
    print(f"[ERROR] {e}")
finally:
    ssh.close()
