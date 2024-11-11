import telebot
from datetime import datetime, timedelta
import threading
import time
import traceback
import logging

# توكن البوت
TOKEN = "6627963661:AAGmFD2TvvuXAzEB1S4q0s70xvCmT-egSUE"

# إنشاء كائن البوت
bot = telebot.TeleBot(TOKEN)

# تحديد التاريخ المستهدف
TARGET_DATE = datetime(2024, 12, 12, 0, 0, 0)

# تخزين معرف الرسالة والـ chat_id للتحديث المستمر
message_id = None
chat_id = None

# إعداد وحدة التسجيل
logging.basicConfig(filename="bot.log", level=logging.ERROR, format="%(asctime)s %(levelname)s: %(message)s")

# دالة لحساب الوقت المتبقي بصيغة "يوم : ساعة : دقيقة"
def get_countdown():
    now = datetime.now()
    time_diff = TARGET_DATE - now
    
    if time_diff.total_seconds() > 0:
        days = time_diff.days
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds % 3600) // 60
        return f"{days} يوم : {hours} ساعة : {minutes} دقيقة"
    else:
        return "تم الإكمال"

# دالة لعرض الرسالة عند بدء المحادثة
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global message_id, chat_id
    chat_id = message.chat.id

    # إنشاء زر شفاف يحتوي على العداد التنازلي
    markup = telebot.types.InlineKeyboardMarkup()
    countdown_text = get_countdown()
    button = telebot.types.InlineKeyboardButton(text=countdown_text, callback_data="update_countdown")
    markup.add(button)
    
    # إرسال رسالة "مرحبا" مع الزر وحفظ معرف الرسالة
    sent_message = bot.send_message(chat_id, "مرحبا", reply_markup=markup)
    message_id = sent_message.message_id

# دالة لتحديث الزر بوقت متبقي جديد
def update_countdown():
    if chat_id and message_id:
        try:
            countdown_text = get_countdown()
            markup = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton(text=countdown_text, callback_data="update_countdown")
            markup.add(button)
            
            # تحديث النص في الزر
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=markup)
        except (telebot.apihelper.ApiException, requests.exceptions.ConnectionError) as e:
            logging.error(f"Error updating countdown: {e}")

# دالة لتشغيل التحديث التلقائي كل دقيقة
def start_timer():
    while True:
        try:
            update_countdown()
        except (telebot.apihelper.ApiException, requests.exceptions.ConnectionError) as e:
            logging.error(f"Error updating countdown: {e}")
            time.sleep(60)  # Wait for 60 seconds before retrying
        time.sleep(60)

# تشغيل التحديث التلقائي في خلفية التطبيق
threading.Thread(target=start_timer).start()

# تشغيل البوت
def telegram_polling():
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)
        except (telebot.apihelper.ApiException, requests.exceptions.ConnectionError) as e:
            logging.error(f"Error polling Telegram: {e}")
            time.sleep(10)  # Wait for 10 seconds before retrying

if __name__ == '__main__':    
    telegram_polling()
