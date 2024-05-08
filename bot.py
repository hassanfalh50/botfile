import os
from telegram import Bot
from telegram import InputFile
from telegram.ext import Updater, CommandHandler
import requests

# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = '6627963661:AAGmFD2TvvuXAzEB1S4q0s70xvCmT-egSUE'

def start(update, context):
    update.message.reply_text("مرحبًا! أرسل /render للقيام بعملية render.")

def render(update, context):
    # Perform rendering process here
    rendered_text = "تم render النص بنجاح!"
    update.message.reply_text(rendered_text)

def download_file(update, context):
    file_url = context.args[0]
    file_name = file_url.split('/')[-1]

    try:
        # Download file from URL
        response = requests.get(file_url)
        with open(file_name, 'wb') as f:
            f.write(response.content)

        # Send file to the bot
        bot = Bot(token=TOKEN)
        bot.send_document(chat_id=update.message.chat_id, document=open(file_name, 'rb'))

        update.message.reply_text("تم إرسال الملف بنجاح!")

        # Delete the file after sending
        os.remove(file_name)

    except Exception as e:
        update.message.reply_text("حدث خطأ أثناء تنزيل أو إرسال الملف.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("render", render))
    dp.add_handler(CommandHandler("download", download_file, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
