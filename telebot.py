#!/usr/bin/env python3
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

import logging
import requests
import yaml

from telegram import Update, ForceReply
from telegram.utils.helpers import escape_markdown
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Used in get_serialstation()
from html import escape as escape_html

# To pass arguments to MessageHandlers
from functools import partial

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


#def echo(update: Update, context: CallbackContext) -> None:
#    """Echo the user message."""
#    update.message.reply_text(update.message.text)


def get_coins(update: Update, context: CallbackContext, coins) -> None:
    """Get BTC and DOGE prices"""
    resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cdogecoin&vs_currencies=usd%2Ceur', headers={"Accept": "application/json"})
    values = resp.json()

    message = ''

    for key in sorted(values.keys()):
        message += key.capitalize() + ':\n'
        for currency in ['eur', 'usd']:
            message += escape_markdown("  {0} = {1}\n".format(currency.upper(), values[key][currency]), version=2)

    message += escape_markdown('\n{0:.3f} BTC are {1:.3f} €'.format(coins['btc'], values['bitcoin']['eur']*coins['btc']), version=2)
    message += escape_markdown('\n{0:.3f} DOGE are {1:.3f} €'.format(coins['doge'], values['dogecoin']['eur']*coins['doge']), version=2)

    #print(message)
    update.message.reply_markdown_v2(message, quote=False)


def get_spec_coin(update: Update, context: CallbackContext) -> None:
    """Get the price of a specified coin in the specified currency"""
    coin = update.message.text.split()[0].lower()
    currency = update.message.text.split()[-1].lower()

    resp = requests.get('https://api.coingecko.com/api/v3/simple/price?ids={0}&vs_currencies={1}'.format(coin, currency), headers={"Accept": "application/json"})
    values = resp.json()

    message = escape_markdown('The current value of {0} is: {1} {2}'.format(coin.capitalize(), values[coin][currency], currency.upper()), version=2)

    #print(message)
    update.message.reply_markdown_v2(message, quote=False)


def get_serialstation(update: Update, context: CallbackContext, api_url) -> None:
    """Generate a link to SerialStation and YouTube for given game"""

    text_part = update.message.text[0:4].upper()
    num_part = update.message.text[-5:]

    serial_station_api = '{0}titles/?title_id_type={1}&title_id_number={2}'.format(api_url, text_part, num_part)

    resp = requests.get(serial_station_api)

    if resp.status_code != 200:
        message = escape_markdown('SerialStation error, response code: {0}'.format(resp.status_code))
    else:
        data = resp.json()
        if data['count'] == 1:
            title = data['results'][0]['name']['default_value']
            escaped_title = escape_html(title).replace(' ', '+')
            message = escape_markdown('{0}-{1}\n{2}\n\nhttps://serialstation.com/titles/{0}/{1}\n\nhttps://www.youtube.com/results?search_query={3}'.format(text_part, num_part, title, escaped_title), version=2)
        elif data['count'] == 0:
            message = escape_markdown('Error: no game found')
        elif data['count'] > 0:
            message = escape_markdown('Error: got more than 1 result')
        else:
            message = escape_markdown('Unkown error, please check journal')

    update.message.reply_markdown_v2(message, quote=False)


def main() -> None:
    """Start the bot."""

    # Read token from config file
    with open(r'/opt/telebot/config.yaml') as config_file:
        data = yaml.safe_load(config_file)

    # Create the Updater and pass it your bot's token.
    updater = Updater(data["telegram_token"], use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^[cC]oins?(\?)*$'), partial(get_coins, coins=data["coins"])))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^[a-zA-Z]+ in [a-zA-Z]+$'), get_spec_coin))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^[a-zA-Z]{4}\-?[0-9]{5}$'), partial(get_serialstation, api_url=data["serialstation_api"])))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
