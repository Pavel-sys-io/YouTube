import telebot
from telebot import types
from pytube import YouTube

bot = telebot.TeleBot('6958478288:AAFQBDOMb_l-doJl60Z-pZ6IzarYkbHmNBU')

def get_start_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🔗 Вставити посилання на відео YouTube")
    btn2 = types.KeyboardButton("ℹ️ Правила використання")
    btn3 = types.KeyboardButton("💡 Приклад використання")
    markup.add(btn1, btn2, btn3)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "👋 Привіт! Я твій бот-помічник!", reply_markup=get_start_keyboard())

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '🔗 Вставити посилання на відео YouTube':
        bot.send_message(message.from_user.id, "Будь ласка, вставте посилання на відео YouTube")
    elif message.text.startswith('https://www.youtube.com/'):
        try:
            youtube_url = message.text
            video = YouTube(youtube_url)
            video_stream = video.streams.filter(progressive=True).first()
            title = video.title
            video_stream.download()  # Download video
            bot.send_document(message.chat.id, open(f'{title}.mp4', 'rb'))
        except Exception as e:
            bot.send_message(message.from_user.id, f'Помилка: {e}')
    elif message.text == 'ℹ️ Правила використання':
        rules_text = "Правила використання:\n1. Не спамити бота повторюваними запитами.\n2.Не використовувати бота для незаконних цілей.\nРозробник бота: Іванов Павло Сергійович.\nТлеграм: https://t.me/pal_palc"
        bot.send_message(message.from_user.id, rules_text, reply_markup=get_start_keyboard())
    elif message.text == '💡 Приклад використання':
        example_text = "Приклад використання:\nНадішли мені посилання на відео з YouTube, і я скачаю його для вас! Приклад посилання: (https://www.youtube.com/watch?v=hLPe_jGmxq). Таке посилання бот не розпізнає, приклад: (https://youtu.be/c5deJSHams)."
        bot.send_message(message.from_user.id, example_text, reply_markup=get_start_keyboard())

bot.polling(none_stop=True, interval=0)