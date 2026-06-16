import requests
import time
import threading

BOT_TOKEN = "8921588455:AAFtySLCxwtEVu8O0JIh2ykJ-njhZsvXEz4"
CHAT_ID = "8949891199"
URL = "https://www.vfsvisaonline.com/Netherlands-Global-Online-Appointment_Zone2/AppScheduling/AppSchedulingGetInfo.aspx?P=wpmn7S46C72lQRV%2f1kDyNQ%3d%3d"

POSITIVE = ["select a date", "please select", "available", "choose", "slot", "book now"]
NEGATIVE = ["no appointment", "not available", "invalid attempt", "no slot", "unavailable", "try again"]

interval = 60
paused = False
last_offset = 0

def send(msg):
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": msg}, timeout=10)

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

def handle_commands():
    global interval, paused, last_offset
    while True:
        try:
            r = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
                params={"offset": last_offset + 1, "timeout": 10}, timeout=15)
            updates = r.json().get("result", [])
            for u in updates:
                last_offset = u["update_id"]
                msg = u.get("message", {}).get("text", "").strip().lower()
                if msg == "/status":
                    send(f"🟢 Running\nInterval: every {interval}s\nPaused: {paused}")
                elif msg == "/pause":
                    paused = True
                    send("⏸ Monitoring paused. Send /resume to restart.")
                elif msg == "/resume":
                    paused = False
                    send("▶️ Monitoring resumed!")
                elif msg.startswith("/interval"):
                    try:
                        secs = int(msg.split()[1])
                        if 30 <= secs <= 3600:
                            interval = secs
                            send(f"✅ Interval set to every {secs} seconds.")
                        else:
                            send("⚠️ Please use a value between 30 and 3600 seconds.")
                    except:
                        send("Usage: /interval 60")
                elif msg == "/help":
                    send(
                        "📋 Commands:\n"
                        "/status — check if bot is running\n"
                        "/pause — pause monitoring\n"
                        "/resume — resume monitoring\n"
                        "/interval 60 — check every 60 seconds\n"
                        "/help — show this message"
                    )
        except: pass
        time.sleep(2)

threading.Thread(target=handle_commands, daemon=True).start()

send("🟢 VFS Monitor live!\nSend /help to see all commands.")

while True:
    if not paused:
        result = check()
        if result == "found":
            send("🎉 APPOINTMENT AVAILABLE! Book now:\n" + URL)
    time.sleep(interval)
