#!/usr/bin/env python

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from content import help_text, start_text, button_names
from bot_token import TOKEN


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(start_text)
    question(update, context)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(help_text)


def question(update: Update, context: CallbackContext) -> None:
    """Send a message when the button is pressed."""
    update.message.reply_photo(photo=open("./data/img1.jpeg", "rb"))
    keyboard = [
        [
            InlineKeyboardButton(button_names[0], callback_data='0'),
            InlineKeyboardButton(button_names[1], callback_data='1'),
        ],
        [
            InlineKeyboardButton(button_names[2], callback_data='2'),
            InlineKeyboardButton(button_names[3], callback_data='3'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("->", reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    # query = update.callback_query

    # # CallbackQueries need to be answered, even if no notification to the user is needed
    # # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    # query.answer()
    # query.edit_message_text(text=f"Selected option: {query.data}")
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