Telegram bot
============

Install
-------

 * `mkdir /opt/telebot/`
 * `cp telebot.py /opt/telebot/`
 * `vim /opt/telebot/config.yaml`
   ```
   ---
   token: "my_bot_token"
   ```
 * `cp telebot.service /etc/systemd/system/`
 * `systemctl daemon-reload`
 * `systemctl enable telebot.service`

Usage
-----

The bot currently understands the following:

RegEx: "" - get the Bitcoin and Dogecoin prices in EUR and USD. For example: **coin** or **Coins?**
Sentence: "$crypto in $currency" - get the specified crypto prices in the specified currency. For example: **monero in huf**

