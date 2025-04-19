from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
from googletrans import Translator

user_lang = {}
user_direction = {}
translator = Translator()

from telegram import ReplyKeyboardRemove

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🇺🇿 O‘zbekcha", callback_data='lang_uz')],
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "🇺🇿 Tilni tanlang\n🇬🇧 Choose language\n🇷🇺 Выберите язык",
        reply_markup=reply_markup
    )


    ReplyKeyboardRemove()


def set_language(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    lang = query.data.split("_")[1]
    user_lang[chat_id] = lang

    if lang == 'uz':
        buttons = [
            [InlineKeyboardButton("🇺🇿 O‘zbekcha → 🇬🇧 Inglizcha", callback_data='dir_uz_en')],
            [InlineKeyboardButton("🇺🇿 O‘zbekcha → 🇷🇺 Ruscha", callback_data='dir_uz_ru')],
            [InlineKeyboardButton("🇬🇧 Inglizcha → 🇺🇿 O‘zbekcha", callback_data='dir_en_uz')],
            [InlineKeyboardButton("🇷🇺 Ruscha → 🇺🇿 O‘zbekcha", callback_data='dir_ru_uz')],
            [InlineKeyboardButton("🇬🇧 Inglizcha → 🇷🇺 Ruscha", callback_data='dir_en_ru')],
            [InlineKeyboardButton("🇷🇺 Ruscha → 🇬🇧 Inglizcha", callback_data='dir_ru_en')],
        ]
        text = "Qaysi yo‘nalishda tarjima qilmoqchisiz?"
    elif lang == 'ru':
        buttons = [
            [InlineKeyboardButton("🇺🇿 Узбекский → 🇬🇧 Английский", callback_data='dir_uz_en')],
            [InlineKeyboardButton("🇺🇿 Узбекский → 🇷🇺 Русский", callback_data='dir_uz_ru')],
            [InlineKeyboardButton("🇬🇧 Английский → 🇺🇿 Узбекский", callback_data='dir_en_uz')],
            [InlineKeyboardButton("🇷🇺 Русский → 🇺🇿 Узбекский", callback_data='dir_ru_uz')],
            [InlineKeyboardButton("🇬🇧 Английский → 🇷🇺 Русский", callback_data='dir_en_ru')],
            [InlineKeyboardButton("🇷🇺 Русский → 🇬🇧 Английский", callback_data='dir_ru_en')],
        ]
        text = "Выберите направление перевода:"
    else:  # English
        buttons = [
            [InlineKeyboardButton("🇺🇿 Uzbek → 🇬🇧 English", callback_data='dir_uz_en')],
            [InlineKeyboardButton("🇺🇿 Uzbek → 🇷🇺 Russian", callback_data='dir_uz_ru')],
            [InlineKeyboardButton("🇬🇧 English → 🇺🇿 Uzbek", callback_data='dir_en_uz')],
            [InlineKeyboardButton("🇷🇺 Russian → 🇺🇿 Uzbek", callback_data='dir_ru_uz')],
            [InlineKeyboardButton("🇬🇧 English → 🇷🇺 Russian", callback_data='dir_en_ru')],
            [InlineKeyboardButton("🇷🇺 Russian → 🇬🇧 English", callback_data='dir_ru_en')],
        ]
        text = "Which translation direction would you like?"

    markup = InlineKeyboardMarkup(buttons)
    query.edit_message_text(text=text, reply_markup=markup)

def set_direction(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat.id
    direction_code = query.data.split("_")[1:]

    src, dest = direction_code
    user_direction[chat_id] = (src, dest)

    lang = user_lang.get(chat_id, 'en')
    if lang == 'uz':
        text = "✍️ Tarjima qilmoqchi bo‘lgan matningizni yuboring:"
    elif lang == 'ru':
        text = "✍️ Введите текст для перевода:"
    else:
        text = "✍️ Send the text you want to translate:"

    query.edit_message_text(text=text, reply_markup=None)

def handle_text(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    text = update.message.text
    direction = user_direction.get(chat_id)

    print(f"User ({chat_id}) said: {text}")

    if not direction:
        update.message.reply_text("❗ Please choose a translation direction first. /start")
        return

    src, dest = direction
    text = update.message.text

    try:
        result = translator.translate(text, src=src, dest=dest)
        update.message.reply_text(result.text)
    except Exception as e:
        update.message.reply_text("❌ An error occurred while translating.")

def main():
    TOKEN = 'YOUR TOKEN'
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(set_language, pattern='^lang_'))
    dp.add_handler(CallbackQueryHandler(set_direction, pattern='^dir_'))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
