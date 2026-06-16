import requests
import time
import os

BOT_TOKEN = "8921588455:AAFtySLCxwtEVu8O0JIh2ykJ-njhZsvXEz4"
CHAT_ID = "8949891199"
URL = "https://www.vfsvisaonline.com/Netherlands-Global-Online-Appointment_Zone2/AppScheduling/AppSchedulingGetInfo.aspx?P=wpmn7S46C72lQRV%2f1kDyNQ%3d%3d"

POSITIVE = ["select a date", "please select", "available", "choose", "slot", "book now"]
NEGATIVE = ["no appointment", "not available", "invalid attempt", "no slot", "unavailable", "try again"]

def send(msg):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg})

def check():
    try:
        proxies = ["https://api.allorigins.win/get?url=", "https://corsproxy.io/?"]
        for proxy in proxies:
            r = requests.get(proxy + requests.utils.quote(URL, safe=""), timeout=15)
            html = r.json().get("contents", "").lower() if "allorigins" in proxy else r.text.lower()
            if len(html) > 200:
                for n in NEGATIVE:
                    if n in html: return "none"
                for p in POSITIVE:
                    if p in html: return "found"
    except: pass
    return "error"

send("🟢 VFS Monitor is live! Checking every 3 minutes...")

while True:
    result = check()
    if result == "found":
        send("🎉 APPOINTMENT AVAILABLE! Book now:\n" + URL)
time.sleep(60)
