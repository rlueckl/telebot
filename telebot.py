#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import yaml
import requests
import logging

from telegram import Update, ForceReply, utils
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def get_coins(update: Update, _: CallbackContext) -> None:
    """Get BTC and DOGE prices"""
    resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cdogecoin&vs_currencies=usd%2Ceur', headers = {"Accept": "application/json"})
    values = resp.json()
    message = ''
    for key in sorted(values.keys()):
        message += key.capitalize() + ':\n'
        for currency in ['eur', 'usd']:
            message += utils.helpers.escape_markdown("  {0} = {1}\n".format(currency.upper(), values[key][currency]), version=2)
    message += utils.helpers.escape_markdown('\n0.082 BTC are {0:.3f} €'.format(values['bitcoin']['eur']*0.08282086), version=2)
    message += utils.helpers.escape_markdown('\n23970.964 DOGE are {0:.3f} €'.format(values['dogecoin']['eur']*23970.96412846), version=2)
    #print(message)
    update.message.reply_markdown_v2(message, quote=False)

def main() -> None:
    with open(r'/opt/telebot/config.yaml') as config_file:
      data = yaml.load(config_file, yaml.SafeLoader)

    print(data)
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(data["token"])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    #dispatcher.add_handler(CommandHandler("coins", get_coins))

    # on non command i.e message - echo the message on Telegram
    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.regex('[cC]oins?(\?)*'), get_coins))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
