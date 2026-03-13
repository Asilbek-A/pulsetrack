#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check backend logs and test login endpoint."""
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
            print(f"    {output[:800]}")
    return output, exit_status

print("=" * 50)
print("  CHECKING LOGIN ERROR")
print("=" * 50)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS, timeout=30,
                allow_agent=False, look_for_keys=False)
    print(f"\n[OK] Connected to {SERVER_IP}\n")

    # Check PM2 logs
    print("[1] Recent backend logs (last 30 lines)...")
    logs, _ = ssh_exec(ssh, "pm2 logs pulsetrack-api --lines 30 --nostream 2>&1 | tail -30", "PM2 logs")

    # Check if backend is running
    print("\n[2] Checking PM2 status...")
    status, _ = ssh_exec(ssh, "pm2 list | grep pulsetrack-api", "PM2 status")

    # Test login endpoint with different payloads
    print("\n[3] Testing login endpoint...")
    
    # Test 1: Valid JSON format
    test1, _ = ssh_exec(ssh, "curl -s -X POST http://localhost:4000/api/auth/login -H 'Content-Type: application/json' -d '{\"email\":\"test@test.com\",\"password\":\"test123\"}'", "Test 1: email login")
    print(f"    Response: {test1[:300]}")
    
    # Test 2: Phone login
    test2, _ = ssh_exec(ssh, "curl -s -X POST http://localhost:4000/api/auth/login -H 'Content-Type: application/json' -d '{\"phone\":\"+998901234567\",\"password\":\"test123\"}'", "Test 2: phone login")
    print(f"    Response: {test2[:300]}")

    # Check database connection
    print("\n[4] Checking database...")
    db_check, _ = ssh_exec(ssh, "cd /var/whoop/backend && cat .env 2>/dev/null | grep -E 'DB_|DATABASE' | head -5", "Database config")

    # Check backend error logs
    print("\n[5] Checking backend error logs...")
    error_logs, _ = ssh_exec(ssh, "pm2 logs pulsetrack-api --err --lines 20 --nostream 2>&1 | tail -20", "Error logs")

    print("\n" + "=" * 50)
    print("  DIAGNOSIS COMPLETE")
    print("=" * 50)

except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
finally:
    ssh.close()
