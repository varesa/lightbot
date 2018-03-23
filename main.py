import os
import logging
from telegram.ext import Updater, CommandHandler
from time import sleep


def register(bot, update):
    """
    Register a new user to receive light events
    """
    bot.send_message(chat_id=update.message.chat_id, text="Not implemented")


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    token = os.environ['TELEGRAM_TOKEN']

    # Initialize the telegram API
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    # Register the command handler
    register_handler = CommandHandler('register', register)
    dispatcher.add_handler(register_handler)

    update.start_polling()


if __name__ == "__main__":
    main()
