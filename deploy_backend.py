#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deploy backend to server."""
import os
import paramiko
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SERVER_IP = "155.212.219.232"
SERVER_USER = "root"
SERVER_PASS = "!vl10982dZm4"
BACKEND_PATH = "/var/whoop/backend"
LOCAL_BACKEND = r"C:\Users\User\Desktop\whoop\backend"

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
print("  DEPLOYING BACKEND")
print("=" * 50)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS, timeout=30,
                allow_agent=False, look_for_keys=False)
    print(f"\n[OK] Connected to {SERVER_IP}\n")

    # Upload backend source files
    print("[1] Uploading backend source files...")
    sftp = ssh.open_sftp()
    
    # Upload src folder
    src_local = os.path.join(LOCAL_BACKEND, "src")
    if os.path.exists(src_local):
        uploaded = 0
        for root, dirs, files in os.walk(src_local):
            for file in files:
                local_path = os.path.join(root, file)
                rel_path = os.path.relpath(local_path, src_local)
                remote_path = os.path.join(BACKEND_PATH, "src", rel_path).replace('\\', '/')
                remote_dir = os.path.dirname(remote_path)
                parts = remote_dir.replace(BACKEND_PATH, '').strip('/').split('/')
                current = BACKEND_PATH
                for part in parts:
                    if part:
                        current = current + '/' + part
                        try:
                            sftp.mkdir(current)
                        except:
                            pass
                sftp.put(local_path, remote_path)
                uploaded += 1
                if uploaded % 10 == 0:
                    print(f"  ✓ Uploaded {uploaded} files...")
        print(f"  ✓ Total: {uploaded} source files")
    
    # Upload config files
    for file in ['package.json', 'package-lock.json', 'tsconfig.json']:
        local_path = os.path.join(LOCAL_BACKEND, file)
        if os.path.exists(local_path):
            remote_path = os.path.join(BACKEND_PATH, file).replace('\\', '/')
            sftp.put(local_path, remote_path)
            print(f"  ✓ {file}")
    
    sftp.close()

    # Install dependencies and build
    print("\n[2] Installing dependencies...")
    ssh_exec(ssh, f"cd {BACKEND_PATH} && npm install", "npm install")
    
    print("\n[3] Building backend...")
    ssh_exec(ssh, f"cd {BACKEND_PATH} && npm run build", "npm build")

    print("\n[4] Restarting backend with PM2...")
    ssh_exec(ssh, "pm2 restart pulsetrack-api || pm2 start /var/whoop/backend/dist/index.js --name pulsetrack-api", "PM2 restart")

    print("\n[5] Testing API endpoint...")
    test_output, _ = ssh_exec(ssh, "curl -s http://localhost:4000/api/auth/login -X POST -H 'Content-Type: application/json' -d '{\"email\":\"test\",\"password\":\"test\"}' | head -3", "Login test")
    if "message" in test_output.lower() or "error" in test_output.lower():
        print("  [OK] API endpoint is responding (even with test credentials)")

    print("\n" + "=" * 50)
    print("  BACKEND DEPLOY COMPLETE")
    print("=" * 50)
    print(f"\n  API: http://{SERVER_IP}/api/")
    print("=" * 50)

except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
finally:
    ssh.close()
