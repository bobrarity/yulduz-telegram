from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler, \
    CallbackQueryHandler
from pydub import AudioSegment
from yulduz_funcs import *

TOKEN = 'TELEGRAM_API_KEY'

# states for conversation handler
LANGUAGE_CHOICE, PROCESSING = range(2)

messages = {
    'start': {
        'en': "Hello! I'm a Yulduz Assistant. Ask any questions! 😊",
        'ru': "Привет! Я ассистент Yulduz. Задавайте любые вопросы! 😊",
        'uz': "Salom! Men Yulduz yordamchisiman. Har qanday savollarni bering! 😊",
    },
    'help': {
        'en': "Send any question in text or voice message. 🤓",
        'ru': "Отправьте любой вопрос текстом или голосовым сообщением. 🤓",
        'uz': "Har qanday savolni matn yoki ovozli xabar orqali yuboring. 🤓",
    },
    'about': {
        'en': "🤖 Yulduz Assistant📚\n\nOverview:\nWelcome to our cutting-edge Assistant Yulduz designed to revolutionize your experience with our online courses...",
        'ru': "🤖 Помощник Yulduz📚\n\nОбзор:\nДобро пожаловать в нашего передового помощника Yulduz, созданного для того, чтобы революционизировать ваш опыт...",
        'uz': "🤖 Yulduz Yordamchisi📚\n\nUmumiy ma'lumot:\nOnlayn kurslarimiz bilan tajribangizni tubdan o'zgartirishga mo'ljallangan ilg'or Yulduz yordamchimizga xush kelibsiz...",
    },
    'wait': {
        'en': "Your message was received ✅.\nProcessing your request... ⌛",
        'ru': "Ваше сообщение получено ✅.\nОбработка вашего запроса... ⌛",
        'uz': "Xabaringiz qabul qilindi ✅.\nSoʻrovingiz koʻrib chiqilmoqda... ⌛",
    }
}

user_data = {}


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🇬🇧 English", callback_data='en'),
         InlineKeyboardButton("🇷🇺 Русский", callback_data='ru'),
         InlineKeyboardButton("🇺🇿 O'zbek", callback_data='uz')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose your language.', reply_markup=reply_markup)
    return LANGUAGE_CHOICE


def language_choice(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_language = query.data
    user_data[query.from_user.id] = user_language
    query.edit_message_text(text=messages['start'][user_language])
    return PROCESSING


def help_command(update: Update, context: CallbackContext):
    user_language = user_data.get(update.effective_user.id, 'en')
    update.message.reply_text(messages['help'][user_language])


def about(update: Update, context: CallbackContext):
    user_language = user_data.get(update.effective_user.id, 'en')
    update.message.reply_text(messages['about'][user_language])


def text_message(update: Update, context: CallbackContext):
    user_language = user_data.get(update.effective_user.id, 'en')  # default to English if not set
    input_text = update.message.text
    response_message = {
        'en': f"[Yulduz]: {english(input_text)}",
        'ru': f"[Yulduz]: {russian(input_text)}",
        'uz': f"[Yulduz]: {uzbek(input_text)}",
    }
    update.message.reply_text(messages['wait'][user_language])

    update.message.reply_text(response_message[user_language])


def voice_message(update: Update, context: CallbackContext):
    user_language = user_data.get(update.effective_user.id, 'en')  # Retrieve the user's language choice

    voice_file = update.message.voice.get_file()
    voice_file_path = 'voice_message.ogg'
    voice_file.download(voice_file_path)

    update.message.reply_text(messages['wait'][user_language])

    audio = AudioSegment.from_ogg(voice_file_path)
    wav_file_path = 'voice_message.wav'
    audio.export(wav_file_path, format='wav')

    stt_function = {'en': english_stt, 'ru': russian_stt, 'uz': uzbek_stt}[user_language]

    update.message.reply_text(f'[Yulduz]: {stt_function(wav_file_path)}')


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE_CHOICE: [CallbackQueryHandler(language_choice)],
            PROCESSING: [
                CommandHandler('help', help_command),
                CommandHandler('about', about),
                MessageHandler(Filters.text & ~Filters.command, text_message),
                MessageHandler(Filters.voice & ~Filters.command, voice_message),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dp.add_handler(conv_handler)

    # bot launch
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
