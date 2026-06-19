# ===================== بوت السلام البسيط =====================
from http.server import BaseHTTPRequestHandler
import json
import requests
import time
import threading

# ===================== توكن البوت =====================
BOT_TOKEN = "8330182703:AAF_Li7LP-6z8jSkVDOVq-fVKa4t2eU3euE"

# ===================== دوال Telegram API =====================
def send_message(chat_id, text):
    """إرسال رسالة"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

def get_updates(offset=None):
    """جلب التحديثات"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    try:
        response = requests.get(url, params=params, timeout=35)
        return response.json().get("result", [])
    except:
        return []

def handle_message(message):
    """معالجة الرسائل - فقط السلام"""
    chat_id = message["chat"]["id"]
    
    if "text" in message:
        text = message["text"].strip()
        
        # كلمات السلام
        salam_words = ["السلام", "سلام", "السلام عليكم", "سلام عليكم", "سلام عليك", "السلام عليك"]
        
        # التحقق من وجود كلمة السلام في النص
        if any(word in text for word in salam_words):
            send_message(chat_id, """
🌿 <b>وَعَلَيْكُمُ السَّلَامُ وَرَحْمَةُ اللَّهِ وَبَرَكَاتُهُ</b>

🌹 أهلاً بك!
""")
        elif text == "/start":
            send_message(chat_id, """
👋 <b>مرحباً بك في بوت السلام!</b>

📌 أرسل لي:
• السلام
• السلام عليكم
• سلام

وسأرد عليك التحية!
""")
        else:
            send_message(chat_id, "👋 قل لي 'السلام' لأرد عليك!")

# ===================== تشغيل البوت =====================
def run_bot():
    """تشغيل البوت"""
    last_update_id = 0
    while True:
        try:
            updates = get_updates(last_update_id + 1)
            for update in updates:
                last_update_id = update["update_id"]
                if "message" in update:
                    handle_message(update["message"])
            time.sleep(1)
        except:
            time.sleep(5)

# بدء تشغيل البوت
threading.Thread(target=run_bot, daemon=True).start()

# ===================== نقطة دخول Vercel =====================
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "running", "bot": "salam_bot"}).encode())
    
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"status":"ok"}')