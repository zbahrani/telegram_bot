from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import requests

TOKEN = '7240596142:AAFJ7KH2x9ifmKViHV0Va3Gn8h2RTXztKsU'
API_KEY = '47f3773ad3ce31296ecf4375516389e9'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('سلام! من ربات شما هستم.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('دستورات موجود: /start، /help ، /weather <شهر> ، /send_message ')

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) == 0:
        await update.message.reply_text('لطفاً نام شهری را وارد کنید. مثال: /weather Tehran')
        return

    city = ' '.join(context.args)
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=fa&units=metric'

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            await update.message.reply_text('شهر یافت نشد! لطفاً نام شهر را به درستی وارد کنید.')
            return

        temp = data['main']['temp']
        weather_description = data['weather'][0]['description']
        await update.message.reply_text(f'وضعیت هوای {city}:\nدمای فعلی: {temp}°C\nتوضیحات: {weather_description}')
    except Exception as e:
        await update.message.reply_text('خطایی پیش آمده است. لطفاً دوباره امتحان کنید.')

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("weather", weather))
    application.run_polling()

if __name__ == '__main__':
    main()