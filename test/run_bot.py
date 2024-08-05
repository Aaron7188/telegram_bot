from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

def start(update, context):
    update.message.reply_text('Hi! I am your bot. How can I help you today?')

def handle_message(update, context):
    user_message = update.message.text
    update.message.reply_text(f'You said: {user_message}')

def main():
    # 使用你的 Telegram Bot Token
    request_kwargs = {
        'proxy_url': 'http://127.0.0.1:7890',  # 替换为你的代理服务器地址

    }
    updater = Updater("7406198136:AAGmZm5LBVVoN3bqbd2voQgb_5dF8tiIOSg", use_context=True, request_kwargs=request_kwargs)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
