#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add /api proxy to Nginx configuration."""
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
            print(f"    {output[:300]}")
    return output, exit_status

print("=" * 50)
print("  FIXING NGINX API PROXY")
print("=" * 50)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS, timeout=30,
                allow_agent=False, look_for_keys=False)
    print(f"\n[OK] Connected to {SERVER_IP}\n")

    # Backup
    print("[1] Backing up nginx config...")
    ssh_exec(ssh, "cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup2", "Backup created")

    # Read current config
    print("\n[2] Reading nginx config...")
    stdin, stdout, stderr = ssh.exec_command("cat /etc/nginx/sites-available/default")
    config = stdout.read().decode('utf-8', errors='replace')

    # Check if /api already exists
    if "location /api" in config:
        print("\n[OK] /api location already exists in config!")
    else:
        print("\n[3] Adding /api proxy location...")
        
        lines = config.split('\n')
        new_lines = []
        location_added = False
        
        for i, line in enumerate(lines):
            # Find location / block
            if 'location /' in line and '{' in line and not location_added:
                new_lines.append(line)
                # Add /api location BEFORE location /
                indent = ' ' * (len(line) - len(line.lstrip()))
                new_lines.append(f"{indent}")
                new_lines.append(f"{indent}    # API proxy to backend")
                new_lines.append(f"{indent}    location /api/ {{")
                new_lines.append(f"{indent}        proxy_pass http://localhost:4000/;")
                new_lines.append(f"{indent}        proxy_http_version 1.1;")
                new_lines.append(f"{indent}        proxy_set_header Upgrade $http_upgrade;")
                new_lines.append(f"{indent}        proxy_set_header Connection 'upgrade';")
                new_lines.append(f"{indent}        proxy_set_header Host $host;")
                new_lines.append(f"{indent}        proxy_set_header X-Real-IP $remote_addr;")
                new_lines.append(f"{indent}        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;")
                new_lines.append(f"{indent}        proxy_set_header X-Forwarded-Proto $scheme;")
                new_lines.append(f"{indent}        proxy_cache_bypass $http_upgrade;")
                new_lines.append(f"{indent}    }}")
                new_lines.append(f"{indent}")
                location_added = True
            else:
                new_lines.append(line)
        
        new_config = '\n'.join(new_lines)
        
        # Write new config
        sftp = ssh.open_sftp()
        with sftp.file('/etc/nginx/sites-available/default', 'w') as f:
            f.write(new_config)
        sftp.close()
        
        print("  [OK] /api location added")

    # Test nginx config
    print("\n[4] Testing nginx configuration...")
    output, exit_code = ssh_exec(ssh, "nginx -t 2>&1", "Nginx test")
    
    if exit_code == 0:
        print("  [OK] Nginx config is valid")
        
        # Reload nginx
        print("\n[5] Reloading nginx...")
        ssh_exec(ssh, "systemctl reload nginx", "Nginx reloaded")
        print("  [OK] Nginx reloaded successfully")
    else:
        print("  [ERROR] Nginx config test failed!")
        print("  Restoring backup...")
        ssh_exec(ssh, "cp /etc/nginx/sites-available/default.backup2 /etc/nginx/sites-available/default", "Backup restored")

    # Test API endpoint
    print("\n[6] Testing API endpoint...")
    test_output, _ = ssh_exec(ssh, "curl -s http://localhost:4000/health 2>&1 | head -5", "Backend health check")
    if "ok" in test_output.lower() or "200" in test_output:
        print("  [OK] Backend is responding")
    else:
        print(f"  [WARNING] Backend response: {test_output[:100]}")

    print("\n" + "=" * 50)
    print("  NGINX API PROXY CONFIGURED")
    print("=" * 50)
    print(f"\n  API endpoint: http://{SERVER_IP}/api/")
    print("  Frontend can now connect to backend!")
    print("=" * 50)

except Exception as e:
    print(f"\n[ERROR] {e}")
finally:
    ssh.close()
