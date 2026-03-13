#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test CORS and API from external request."""
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
print("  TESTING CORS AND API")
print("=" * 50)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(SERVER_IP, username=SERVER_USER, password=SERVER_PASS, timeout=30,
                allow_agent=False, look_for_keys=False)
    print(f"\n[OK] Connected to {SERVER_IP}\n")

    # Test with CORS headers
    print("[1] Testing API with CORS headers...")
    test_cors, _ = ssh_exec(ssh, """curl -s -X POST http://localhost:4000/api/auth/login \\
      -H 'Content-Type: application/json' \\
      -H 'Origin: http://155.212.219.232' \\
      -H 'Access-Control-Request-Method: POST' \\
      -d '{\"email\":\"test@test.com\",\"password\":\"test123\"}' -v 2>&1 | grep -E '(HTTP|message|CORS|Access-Control)'""", "CORS test")

    # Check backend CORS config
    print("\n[2] Checking backend CORS configuration...")
    cors_config, _ = ssh_exec(ssh, "grep -A 5 'cors' /var/whoop/backend/src/index.ts", "CORS config")

    # Test direct API call
    print("\n[3] Testing direct API call...")
    direct_test, _ = ssh_exec(ssh, "curl -s -X POST http://localhost:4000/api/auth/login -H 'Content-Type: application/json' -d '{\"email\":\"test@test.com\",\"password\":\"test123\"}'", "Direct test")
    print(f"    Response: {direct_test}")

    # Check Nginx CORS headers
    print("\n[4] Checking Nginx CORS headers...")
    nginx_cors, _ = ssh_exec(ssh, "grep -i 'cors\\|access-control' /etc/nginx/sites-available/default", "Nginx CORS")

    print("\n" + "=" * 50)
    print("  CORS TEST COMPLETE")
    print("=" * 50)

except Exception as e:
    print(f"\n[ERROR] {e}")
finally:
    ssh.close()
