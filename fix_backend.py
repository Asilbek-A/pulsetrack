#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix backend - kill old processes and restart."""
import paramiko
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SERVER_IP = "155.212.219.232"
SERVER_USER = "root"
SERVER_PASS = "!vl10982dZm4"
BACKEND_PATH = "/var/whoop/backend"

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
print("  FIXING BACKEND")
print("=" * 50)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS, timeout=30,
                allow_agent=False, look_for_keys=False)
    print(f"\n[OK] Connected to {SERVER_IP}\n")

    # Stop PM2 process
    print("[1] Stopping PM2 process...")
    ssh_exec(ssh, "pm2 stop pulsetrack-api", "Stop PM2")
    ssh_exec(ssh, "pm2 delete pulsetrack-api", "Delete PM2")

    # Kill any process on port 4000
    print("\n[2] Killing processes on port 4000...")
    ssh_exec(ssh, "fuser -k 4000/tcp 2>/dev/null || lsof -ti:4000 | xargs kill -9 2>/dev/null || echo 'No process on port 4000'", "Kill port 4000")

    # Wait a moment
    import time
    time.sleep(2)

    # Verify port is free
    print("\n[3] Verifying port 4000 is free...")
    port_check, _ = ssh_exec(ssh, "netstat -tuln | grep :4000 || ss -tuln | grep :4000 || echo 'Port 4000 is free'", "Port check")

    # Rebuild backend
    print("\n[4] Rebuilding backend...")
    ssh_exec(ssh, f"cd {BACKEND_PATH} && npm run build", "Build backend")

    # Start backend with PM2
    print("\n[5] Starting backend with PM2...")
    ssh_exec(ssh, f"cd {BACKEND_PATH} && pm2 start dist/index.js --name pulsetrack-api", "Start PM2")
    ssh_exec(ssh, "pm2 save", "Save PM2")

    # Wait for startup
    time.sleep(3)

    # Check status
    print("\n[6] Checking backend status...")
    status, _ = ssh_exec(ssh, "pm2 list | grep pulsetrack-api", "PM2 status")
    
    # Test endpoint
    print("\n[7] Testing API endpoint...")
    test, _ = ssh_exec(ssh, "curl -s http://localhost:4000/api/auth/login -X POST -H 'Content-Type: application/json' -d '{\"email\":\"test\",\"password\":\"test\"}' | head -5", "Login test")
    print(f"    Response: {test[:200]}")

    # Check logs
    print("\n[8] Recent logs...")
    logs, _ = ssh_exec(ssh, "pm2 logs pulsetrack-api --lines 10 --nostream 2>&1 | tail -10", "Recent logs")

    print("\n" + "=" * 50)
    print("  BACKEND FIX COMPLETE")
    print("=" * 50)
    print(f"\n  API: http://{SERVER_IP}/api/")
    print("=" * 50)

except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
finally:
    ssh.close()
