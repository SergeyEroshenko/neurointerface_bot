#!/usr/bin/env python

import os
from glob import glob
import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from content import help_text, start_text, button_names
from bot_token import TOKEN
from settings import DATA_PATH


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(start_text)
    question(update, context)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(help_text)


def question(update: Update, context: CallbackContext) -> None:
    """Send a message when the button is pressed."""
    files_list = sorted(glob(os.path.join(DATA_PATH, "*.*")))
    file = random.choice(files_list)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(file, "rb"))
    keyboard = [
        [
            InlineKeyboardButton(button_names[0], callback_data=button_names[0]),
            InlineKeyboardButton(button_names[1], callback_data=button_names[1]),
        ],
        [
            InlineKeyboardButton(button_names[2], callback_data=button_names[2]),
            InlineKeyboardButton(button_names[3], callback_data=button_names[3]),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="->", reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Selected option: {query.data}")

    question(update, context)


def main() -> None:
    """Start the bot."""
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    logger = logging.getLogger(__name__)
    main()