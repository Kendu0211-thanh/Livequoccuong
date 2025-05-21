import requests
import time

# Telegram bot token và chat ID của con
BOT_TOKEN = "7673301496:AAF-TV9j4xLhZbnbseKiJkepuwmVHL__a9A"
CHAT_ID = "5922342911"

# Gửi tin nhắn test khi bot khởi động
def send_startup_message():
    message = "✅ Bot đã hoạt động! Đây là tin nhắn test."
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

# Chạy bot
if __name__ == "__main__":
    send_startup_message()
    while True:
        time.sleep(60)  # Cho bot chạy mãi để tránh bị Render tắt
