#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test backend API endpoints."""
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
print("  TESTING BACKEND API ENDPOINTS")
print("=" * 50)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS, timeout=30,
                allow_agent=False, look_for_keys=False)
    print(f"\n[OK] Connected to {SERVER_IP}\n")

    # Test health endpoint
    print("[1] Testing /health endpoint...")
    health, _ = ssh_exec(ssh, "curl -s http://localhost:4000/health", "Health check")
    print(f"    Response: {health}")

    # Test login endpoint (GET to see if it exists)
    print("\n[2] Testing /api/auth/login endpoint...")
    login_test, _ = ssh_exec(ssh, "curl -s -X POST http://localhost:4000/api/auth/login -H 'Content-Type: application/json' -d '{\"email\":\"test@test.com\",\"password\":\"test\"}'", "Login test")
    print(f"    Response: {login_test[:200]}")

    # Check backend routes
    print("\n[3] Checking backend routes file...")
    backend_path = "/var/whoop/backend"
    routes_check, _ = ssh_exec(ssh, f"find {backend_path} -name '*.ts' -o -name '*.js' | grep -E '(route|auth|login)' | head -5", "Route files")
    
    # Check backend main file
    print("\n[4] Checking backend main file...")
    main_file, _ = ssh_exec(ssh, f"ls -la {backend_path}/src/*.ts {backend_path}/src/*.js {backend_path}/dist/*.js 2>/dev/null | head -10", "Backend files")

    # Check backend package.json for routes
    print("\n[5] Checking backend structure...")
    package_json, _ = ssh_exec(ssh, f"cat {backend_path}/package.json 2>/dev/null | grep -A 5 -B 5 'main\\|start'", "Package.json")

    print("\n" + "=" * 50)
    print("  API TEST COMPLETE")
    print("=" * 50)

except Exception as e:
    print(f"\n[ERROR] {e}")
finally:
    ssh.close()
