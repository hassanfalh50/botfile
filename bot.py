from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from telegram.ext import Updater, MessageHandler, Filters

# تكوين مصادقة جوجل
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # يتيح للمستخدم تسجيل الدخول عن طريق متصفح الويب المحلي

# إنشاء مركز تحميل Google Drive
drive = GoogleDrive(gauth)

# معالج الرسائل للتحميل والتحميل إلى Google Drive
def file_handler(update, context):
    # الحصول على معرّف الملف واسمه
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    
    # تنزيل الملف إلى مجلد مؤقت باستخدام مكتبة python-telegram-bot
    file_path = context.bot.get_file(file_id).download()
    
    # تحميل الملف إلى Google Drive
    gfile = drive.CreateFile({'title': file_name})
    gfile.SetContentFile(file_path)
    gfile.Upload()
    
    update.message.reply_text("تم تحميل الملف بنجاح إلى Google Drive!")

def main():
    # تكوين التليجرام الخاص بك
    updater = Updater("6627963661:AAGmFD2TvvuXAzEB1S4q0s70xvCmT-egSUE", use_context=True)
    dp = updater.dispatcher

    # إضافة معالج الرسائل للتحميل
    dp.add_handler(MessageHandler(Filters.document, file_handler))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
