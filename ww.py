import subprocess
import re
import os
import time
from git import Repo

# مسار المجلد
repo_path = r"D:\fgf\New folder"
link_file = os.path.join(repo_path, "link.txt")

def update_github(new_url):
    try:
        repo = Repo(repo_path)
        with open(link_file, "w") as f:
            f.write(new_url)
        # رفع الملف تلقائياً
        repo.git.add(link_file)
        repo.git.commit('-m', 'Update Tunnel Link')
        repo.remotes.origin.push()
        print(f"تم رفع الرابط: {new_url}")
    except Exception as e:
        print(f"خطأ في الرفع: {e}")

def run():
    # تشغيل النفق
    proc = subprocess.Popen(["cloudflared", "tunnel", "--url", "http://localhost:5244"], 
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        match = re.search(r"https://[\w-]+\.trycloudflare\.com", line)
        if match:
            update_github(match.group(0))
            break # تحديث واحد يكفي في البداية

while True:
    run()
    time.sleep(60) # تحديث كل دقيقة