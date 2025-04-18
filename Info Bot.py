#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
LANGUAGE, FIRSTNAME, SURNAME, AGE, GENDER, CITY =range(6)

messages_en={
    "start": "Welcome! Let's fill out your info.\nWhat is your first name?",
    "firstname": "Great! What is your surname?",
    "surname": "How old are you?",
    "age": "Please enter your age:",
    "gender": "What is your gender?",
    "male": "Male",
    "female": "Female",
    "city": "Which city are you in currently?",
    "thank_you": "✅ Thank you for the info!\n\n"
                "Firstname: {firstname}\n"
                "Surname: {surname}\n"
                "Age: {age}\n"
                "Gender: {gender}\n"
                "City: {city}\n",
    "invalid_age": "Please enter a valid age (numbers only).",
    "cancel":"Conversation canceled. Bye!"
}

messages_uz={
    "start": "Xush kelibsiz! Ma'lumotlaringizni to'ldirishni boshlaymiz.\nIsmingizni kiriting:",
    "firstname": "Ajoyib! Familiyangizni kiriting:",
    "surname": "Yoshingizni kiriting:",
    "age": "Iltimos, yoshingizni kiriting:",
    "gender": "Jinsingizni tanlang:",
    "male": "Erkak",
    "female": "Ayol",
    "city": "Hozirda qaysi shaharda yashayapsiz?",
    "thank_you": "✅ Ma'lumotlar uchun rahmat!\n\n"
                "Ismingiz: {firstname}\n"
                "Familiyangiz: {surname}\n"
                "Yoshingiz: {age}\n"
                "Jinsingiz: {gender}\n"
                "Shaharingiz: {city}\n",
    "invalid_age": "Iltimos, yoshni to'g'ri formatda kiriting (faqat raqamlar).",
    "cancel":"Bekor qilindi. Sog' bo'ling"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["English"], ["Uzbek"]]
    await update.message.reply_text(
        "Please, select language / Iltimos, tilni tanlang:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
    return LANGUAGE

async def language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_language = update.message.text
    if user_language == "English":
        context.user_data["language"] = "en"
        await update.message.reply_text(messages_en["start"])
        return FIRSTNAME
    elif user_language == "Uzbek":
        context.user_data["language"] = "uz"
        await update.message.reply_text(messages_uz["start"])
        return FIRSTNAME
    else:
        await update.message.reply_text("Invalid selection. Please choose English or Uzbek.")
        return LANGUAGE

async def firstname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    language=context.user_data.get("language","en")
    context.user_data["firstname"] = update.message.text
    if language == "en":
        await update.message.reply_text(messages_en["firstname"])
    else:
        await update.message.reply_text(messages_uz["firstname"])
    return SURNAME


async def surname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    language = context.user_data.get("language", "en")
    context.user_data["surname"] = update.message.text
    if language == "en":
        await update.message.reply_text(messages_en["surname"])
    else:
        await update.message.reply_text(messages_uz["surname"])

    return AGE


async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    language = context.user_data.get("language", "en")
    user_age = update.message.text
    if user_age.isdigit():
        context.user_data["age"] = user_age
        if language == "en":
            reply_keyboard = [[messages_en["male"], messages_en["female"]]]
            await update.message.reply_text(messages_en["gender"], reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
        else:
            reply_keyboard = [[messages_uz["male"], messages_uz["female"]]]  # Corrected this line
            await update.message.reply_text(messages_uz["gender"], reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

        return GENDER
    else:
        if language == "en":
            await update.message.reply_text(messages_en["invalid_age"])
        else:
            await update.message.reply_text(messages_uz["invalid_age"])
        return AGE

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    language = context.user_data.get("language", "en")
    context.user_data["gender"] = update.message.text
    if language == "en":
        await update.message.reply_text(messages_en["city"])
    else:
        await update.message.reply_text(messages_uz["city"])

    return CITY


async def city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    language = context.user_data.get("language", "en")
    context.user_data["city"] = update.message.text
    data=context.user_data
    if language == "en":
        await update.message.reply_text(messages_en["thank_you"].format(
            firstname=data["firstname"],
            surname=data["surname"],
            age=data["age"],
            gender=data["gender"],
            city=data["city"],
        ))
    else:
        await update.message.reply_text(messages_uz["thank_you"].format(
            firstname=data["firstname"],
            surname=data["surname"],
            age=data["age"],
            gender=data["gender"],
            city=data["city"],
        ))

    print(context.user_data)
    return ConversationHandler.END



async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if language == "en":
        await update.message.reply_text(messages_en["cancel"])
    else:
        await update.message.reply_text(messages_uz["cancel"])
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7569168658:AAHBheOG7hZI-ks65R174Ad9nBMj419on5A").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE:[ MessageHandler(filters.TEXT & ~filters.COMMAND, language)],
            FIRSTNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, firstname)],
            SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, surname)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],
            GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, gender)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, city)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
