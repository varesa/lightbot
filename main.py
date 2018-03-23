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
    logger = logging.getLogger("lightbot")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    logger.info("Starting up")

    token = os.environ['TELEGRAM_TOKEN']

    # Initialize the telegram API
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    # Register the command handler
    register_handler = CommandHandler('register', register)
    dispatcher.add_handler(register_handler)

    logger.info("Entering loop")

    updater.start_polling()


if __name__ == "__main__":
    main()
