#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configure Nginx for Flutter web SPA routing."""
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
            print(f"    {output[:200]}")
    return output, exit_status

print("=" * 50)
print("  CONFIGURING NGINX FOR FLUTTER WEB")
print("=" * 50)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS, timeout=30,
                allow_agent=False, look_for_keys=False)
    print(f"\n[OK] Connected to {SERVER_IP}\n")

    # Backup current config
    print("[1] Backing up current nginx config...")
    ssh_exec(ssh, "cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup", "Backup created")

    # Read current config
    print("\n[2] Reading current nginx config...")
    stdin, stdout, stderr = ssh.exec_command("cat /etc/nginx/sites-available/default")
    current_config = stdout.read().decode('utf-8', errors='replace')

    # Check if already configured
    if "try_files $uri $uri/ /index.html;" in current_config:
        print("\n[OK] Nginx already configured for SPA routing!")
    else:
        print("\n[3] Updating nginx config for SPA routing...")
        
        # Find location / block and update it
        lines = current_config.split('\n')
        new_lines = []
        in_location = False
        location_updated = False
        
        for i, line in enumerate(lines):
            if 'location /' in line and '{' in line:
                in_location = True
                new_lines.append(line)
            elif in_location and line.strip() == '}':
                if not location_updated:
                    # Add try_files before closing brace
                    indent = ' ' * (len(line) - len(line.lstrip()))
                    new_lines.append(f"{indent}    try_files $uri $uri/ /index.html;")
                new_lines.append(line)
                in_location = False
                location_updated = True
            elif in_location and 'try_files' in line:
                # Already has try_files, keep it
                new_lines.append(line)
                location_updated = True
            else:
                new_lines.append(line)
        
        new_config = '\n'.join(new_lines)
        
        # Write new config
        sftp = ssh.open_sftp()
        with sftp.file('/etc/nginx/sites-available/default', 'w') as f:
            f.write(new_config)
        sftp.close()
        
        print("  [OK] Config updated")

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
        ssh_exec(ssh, "cp /etc/nginx/sites-available/default.backup /etc/nginx/sites-available/default", "Backup restored")

    print("\n" + "=" * 50)
    print("  NGINX CONFIGURATION COMPLETE")
    print("=" * 50)
    print(f"\n  Web app: http://{SERVER_IP}/")
    print("  Flutter routes should now work correctly!")
    print("=" * 50)

except Exception as e:
    print(f"\n[ERROR] {e}")
finally:
    ssh.close()
