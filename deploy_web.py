#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deploy Flutter web build to Beget VPS."""
import os
import sys
import paramiko

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Server credentials
SERVER_IP = "155.212.219.232"
SERVER_USER = "root"
SERVER_PASS = "!vl10982dZm4"
WEB_PATH = "/var/www/html"  # Standard Apache/Nginx web root

APP_ROOT = r"C:\Users\User\Desktop\whoop"

def ssh_exec(ssh, cmd, desc=""):
    """Execute SSH command and print output."""
    stdin, stdout, stderr = ssh.exec_command(cmd)
    exit_status = stdout.channel.recv_exit_status()
    output = stdout.read().decode('utf-8', errors='replace').strip()
    if desc:
        print(f"  [{desc}] {output[:200]}")
    return output

def main():
    print("=" * 50)
    print("  DEPLOYING FLUTTER WEB BUILD TO BEGET VPS")
    print("=" * 50)

    # 1. Connect to server
    print("\n[1/3] Connecting to server...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(
            SERVER_IP,
            username=SERVER_USER,
            password=SERVER_PASS,
            timeout=30,
            allow_agent=False,
            look_for_keys=False,
            banner_timeout=30
        )
        print(f"  [OK] Connected to {SERVER_IP}")
    except Exception as e:
        print(f"  [ERROR] Connection failed: {e}")
        print("  Trying alternative method...")
        return

    try:
        # 2. Check web directory
        print("\n[2/3] Checking web directory...")
        ssh_exec(ssh, f"test -d {WEB_PATH} && echo YES || echo NO", "Web directory exists")
        ssh_exec(ssh, f"mkdir -p {WEB_PATH}", "Ensuring web directory")

        # 3. Upload Flutter web build
        print("\n[3/3] Uploading Flutter web build...")
        web_build_path = os.path.join(APP_ROOT, "whoop_app", "build", "web")
        
        if not os.path.exists(web_build_path):
            print(f"  ✗ Build directory not found: {web_build_path}")
            print("  Run 'flutter build web --release --base-href /' first!")
            return

        print(f"  Uploading from: {web_build_path}")
        print(f"  Uploading to: {WEB_PATH}")

        # Clear old files
        ssh_exec(ssh, f"rm -rf {WEB_PATH}/*", "Clearing old files")

        # Upload files using SFTP
        sftp = ssh.open_sftp()
        try:
            uploaded = 0
            for root, dirs, files in os.walk(web_build_path):
                for file in files:
                    local_path = os.path.join(root, file)
                    rel_path = os.path.relpath(local_path, web_build_path)
                    remote_path = os.path.join(WEB_PATH, rel_path).replace('\\', '/')
                    remote_dir = os.path.dirname(remote_path)
                    # Create remote directory recursively
                    parts = remote_dir.replace(WEB_PATH, '').strip('/').split('/')
                    current = WEB_PATH
                    for part in parts:
                        if part:
                            current = current + '/' + part
                            try:
                                sftp.mkdir(current)
                            except:
                                pass  # Directory might already exist
                    # Upload file
                    sftp.put(local_path, remote_path)
                    uploaded += 1
                    if uploaded % 10 == 0:
                        print(f"  ✓ Uploaded {uploaded} files...")
            print(f"  ✓ Total: {uploaded} files uploaded")
        finally:
            sftp.close()

        print("\n" + "=" * 50)
        print("  DEPLOY COMPLETE!")
        print("=" * 50)
        print(f"\n  Web app:  http://{SERVER_IP}/")
        print(f"  (or your domain if configured)")
        print("=" * 50)

    finally:
        ssh.close()

if __name__ == "__main__":
    main()
