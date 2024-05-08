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

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("render", render))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
