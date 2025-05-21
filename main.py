import time
import re
import requests
from telegram import Bot
from threading import Thread
from flask import Flask

# ==== CẤU HÌNH ====
TELEGRAM_TOKEN = "7673301496:AAF-TV9j4xLhZbnbseKiJkepuwmVHL__a9A"
CHAT_ID = "5922342911"
TIKTOK_USERNAME = "0211quoccuong"

bot = Bot(token=TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot đang chạy ngon lành!"

def is_live(username):
    try:
        url = f'https://www.tiktok.com/@{username}/live'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        html = response.text

        if '"isLive":true' in html:
            return True

        pattern = re.compile(
            r'<[^>]+class=["\'][^"\']*(live|badge)[^"\']*["\'][^>]*>\s*live\s*</[^>]+>',
            re.IGNORECASE
        )
        if pattern.search(html):
            return True

    except Exception as e:
        print(f"Lỗi khi kiểm tra live: {e}")
    return False

def run_bot():
    print("Bot bắt đầu theo dõi idol live TikTok...")
    was_live = False
    while True:
        try:
            live_now = is_live(TIKTOK_USERNAME)
            if live_now and not was_live:
                bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"🛎️ {TIKTOK_USERNAME} đang LIVE trên TikTok! Vào xem ngay: https://www.tiktok.com/@{TIKTOK_USERNAME}/live"
                )
                was_live = True
            elif not live_now:
                was_live = False
        except Exception as e:
            print(f"Lỗi vòng lặp: {e}")
        time.sleep(15)  # Kiểm tra mỗi 15 giây

if __name__ == "__main__":
    # Chạy bot trong luồng riêng
    Thread(target=run_bot).start()
    # Mở web server
    app.run(host="0.0.0.0", port=10000)
