Telegram bot
============

Based on [echobot.py](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py) from [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

Install
-------

 * `pip install python-telegram-bot --upgrade`
 * `mkdir /opt/telebot/`
 * `cp telebot.py /opt/telebot/`
 * `vim /opt/telebot/config.yaml`
   ```yaml
   ---
   token: "my_bot_token"
   ```
 * `cp telebot.service /etc/systemd/system/`
 * `systemctl daemon-reload`
 * `systemctl enable telebot.service`

Usage
-----

The bot currently understands the following:

_RegEx:_ `[cC]oins?(\?)*` - to get the Bitcoin and Dogecoin prices in EUR and USD.
For example: **coin** or **Coins?**

_Sentence:_ `$CRYPTO in $CURRENCY` - to get the specified crypto prices in the specified currency.
For example: **monero in huf** or **Bitcoin in USD**

