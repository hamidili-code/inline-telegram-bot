import os
from flask import Flask, request
from dotenv import load_dotenv

# فراخوانی تابع از پوشه و فایل مجزا
from message_handler.message_handler import process_inline_query

load_dotenv()

# ۱. دریافت متغیرها از .env (افزودن SITE_URL که قبلاً تعریف نشده بود)
BOT_TOKEN = os.getenv("BOT_TOKEN")
SITE_URL = os.getenv("SITE_URL", "https://shelow.ir")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in .env file.")

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # ۲. دریافت ایمن دیتای JSON (جلوگیری از کرش در صورت خالی بودن درخواست)
    data = request.get_json(silent=True)
    
    if data and "inline_query" in data:
        # ۳. مدیریت خطا (Try-Except) برای جلوگیری از ارسال کد 500 به تلگرام
        try:
            process_inline_query(data["inline_query"], BOT_TOKEN, SITE_URL)
        except Exception as e:
            print(f"Error executing process_inline_query: {e}")

    # ۴. پاسخ سریع 200 OK به تلگرام
    return "OK", 200