import os
import subprocess
import time
import shutil
import sys
import re
from threading import Thread

def install_pkg(pkg):
    if shutil.which("pkg"):
        os.system(f"pkg install {pkg} -y")
    elif shutil.which("apt"):
        os.system(f"sudo apt install {pkg} -y")

def check_installations():
    if not shutil.which("php"):
        print("🚀 Installing PHP...")
        install_pkg("php")
    else:
        print("✅ PHP already installed.")

    if not shutil.which("cloudflared"):
        print("🚀 Installing Cloudflared...")
        install_pkg("cloudflared")
    else:
        print("✅ Cloudflared already installed.")

def create_files():
    if not os.path.exists("index.html"):
        with open("index.html", "w") as f:
            f.write('''<h1>DarkX Live Upload Server</h1>
<form action="upload.php" method="post" enctype="multipart/form-data">
  <input type="file" name="file">
  <input type="submit" value="Upload">
</form>''')

    if not os.path.exists("log.php"):
        with open("log.php", "w") as f:
            f.write("""<?php
if(isset($_FILES['file'])){
    move_uploaded_file($_FILES['file']['tmp_name'], $_FILES['file']['name']);
    echo "✅ File Uploaded!";
}
?>""")

def run_php_server():
    print("🌀 Starting PHP server at http://localhost:8080")
    return subprocess.Popen(["php", "-S", "localhost:8080"])

def run_cloudflared():
    print("🌐 Starting cloudflared tunnel...")

    # Start cloudflared process in background
    process = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", "http://localhost:8080"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Read stdout live
    public_url = None
    for line in process.stdout:
        if "trycloudflare.com" in line:
            match = re.search(r"(https://[a-zA-Z0-9.-]+\.trycloudflare\.com)", line)
            if match:
                public_url = match.group(1)
                print(f"\n🔗 Public Link: {public_url}")
                break

    if not public_url:
        print("❌ Tunnel failed to start or link not found!")

    return process  # returning process in case user wants to stop later

def main():
    check_installations()
    create_files()
    php_process = run_php_server()
    time.sleep(2)

    try:
        tunnel = run_cloudflared()
        print("✅ All set! Server is live.")
        print("Press CTRL+C to stop...")
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("🛑 Exiting and killing servers...")
    finally:
        php_process.terminate()
        tunnel.terminate()

if __name__ == "__main__":
    main()
