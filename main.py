import hashlib
import logging
import os
import requests
from telegram.ext import Updater, CommandHandler
from time import sleep


# Setup logging

logger = logging.getLogger("lightbot")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


def start(bot, update):
    """
    Handler for the /start command. Send instructions
    """
    logger.info("Received /start. Chat ID:" + str(update.message.chat_id))
    logger.info("Sending instructions")

    bot.send_message(chat_id=update.message.chat_id, text="Hello. Type /register to start receiving notifications about light changes")


def register(bot, update):
    """
    Register a new user to receive light events
    """
    logger.info("Received /register. Chat ID: " + str(update.message.chat_id))

    bot.send_message(chat_id=update.message.chat_id, text="Not implemented")


URL = "http://castor.cc.tut.fi/lights.php"

def get():
    r = requests.get(URL)
    h = hashlib.sha1()
    h.update(r.text.encode())

    return h.hexdigest()


def main():
    logger.info("Starting up")

    token = os.environ['TELEGRAM_TOKEN']

    # Initialize the telegram API
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    # Register the command handlers
    start_handler = CommandHandler('start', start)
    register_handler = CommandHandler('register', register)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(register_handler)

    logger.info("Entering loop")

    updater.start_polling()


if __name__ == "__main__":
    main()
