import time
import re
import requests
from telegram import Bot

# ==== CẤU HÌNH ====
TELEGRAM_TOKEN = "7673301496:AAF-TV9j4xLhZbnbseKiJkepuwmVHL__a9A"
CHAT_ID = "5922342911"
TIKTOK_USERNAME = '0211quoccuong'  # Thay bằng username idol TikTok thật của con, không có dấu @

bot = Bot(token=TELEGRAM_TOKEN)

def is_live(username):
    """
    Kiểm tra idol có đang live TikTok không bằng cách:
    - Tìm chuỗi "isLive":true trong HTML
    - Hoặc tìm thẻ HTML có class chứa 'live' hoặc 'badge' và có chữ 'live' bên trong (khung đỏ live)
    """
    try:
        url = f'https://www.tiktok.com/@{username}/live'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        html = response.text

        # Kiểm tra chuỗi "isLive":true
        if '"isLive":true' in html:
            return True

        # Kiểm tra thẻ có chữ LIVE trong khung đỏ
        pattern = re.compile(
            r'<[^>]+class=["\'][^"\']*(live|badge)[^"\']*["\'][^>]*>\s*live\s*</[^>]+>', 
            re.IGNORECASE
        )
        if pattern.search(html):
            return True

    except Exception as e:
        print(f"Lỗi khi kiểm tra live: {e}")
    return False

def main():
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
        time.sleep(10)  # Kiểm tra mỗi 10 giây

if __name__ == "__main__":
    main()
