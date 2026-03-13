#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check backend routes configuration."""
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
            print(f"    {output[:800]}")
    return output, exit_status

print("=" * 50)
print("  CHECKING BACKEND ROUTES")
print("=" * 50)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS, timeout=30,
                allow_agent=False, look_for_keys=False)
    print(f"\n[OK] Connected to {SERVER_IP}\n")

    # Check main index.ts
    print("[1] Checking main index.ts...")
    main_file, _ = ssh_exec(ssh, f"cat {BACKEND_PATH}/src/index.ts", "Main file")

    # Check auth routes
    print("\n[2] Checking auth routes...")
    auth_routes, _ = ssh_exec(ssh, f"cat {BACKEND_PATH}/src/modules/auth/auth.routes.ts", "Auth routes")

    # Test different endpoints
    print("\n[3] Testing different login endpoints...")
    endpoints = [
        "/auth/login",
        "/api/auth/login",
        "/users/login",
        "/login"
    ]
    
    for endpoint in endpoints:
        test, _ = ssh_exec(ssh, f"curl -s -X POST http://localhost:4000{endpoint} -H 'Content-Type: application/json' -d '{{\"email\":\"test\",\"password\":\"test\"}}' | head -3", f"Testing {endpoint}")

    print("\n" + "=" * 50)
    print("  ROUTES CHECK COMPLETE")
    print("=" * 50)

except Exception as e:
    print(f"\n[ERROR] {e}")
finally:
    ssh.close()
