import hashlib
import logging
import os
import requests
from telegram.ext import Updater, CommandHandler
from time import sleep

# Constants

LOG_LEVEL = logging.DEBUG

URL = "http://castor.cc.tut.fi/lights.php"
LIGHTS_OFF = "7d13e0469c6d61c36814fff4a3b3cafa1d34a3fa"

POLL_INTERVAL = 180

# Setup logging

logger = logging.getLogger("lightbot")
logger.setLevel(LOG_LEVEL)
handler = logging.StreamHandler()
handler.setLevel(LOG_LEVEL)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Message handlers

def start(bot, update):
    """
    Handler for the /start command. Send instructions
    """
    logger.info("Received /start. Chat ID:" + str(update.message.chat_id))
    logger.info("Sending instructions")

    bot.send_message(chat_id=update.message.chat_id, text="Hello. Type /register to start receiving notifications about light changes")

registered = []

def register(bot, update):
    """
    Register a new user to receive light events
    """
    logger.info("Received /register. Chat ID: " + str(update.message.chat_id))

    registered.append(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text="You will now receive events until the bot is restarted (TBF)")

# Lamp polling

def get_light_state():
    r = requests.get(URL)
    h = hashlib.sha1()
    h.update(r.text.encode())

    return h.hexdigest() != LIGHTS_OFF


def lights_change(new_state, bot):
    logger.info("Lights state changed to: " + str(new_state))
    for chat in registered:
        logger.info("Sending message to " + str(chat))
        bot.send_message(chat_id=chat, text="Lights changed to: " + str(new_state))


# Main loop

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

    light_state = None

    while True:
        new_state = get_light_state()
        logger.debug("Lights: " + str(new_state))

        if light_state is None:
            light_state = new_state
        else:
            if new_state is not light_state:
                lights_change(new_state, updater.bot)
                light_state = new_state

        sleep(POLL_INTERVAL)

    updater.stop()

if __name__ == "__main__":
    main()
