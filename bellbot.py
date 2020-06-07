import sys
import os
import time
import datetime
import subprocess

import telegram


CONFIG_FILE = os.path.expanduser("~/.config/bellbot")


def load_config():
    with open(CONFIG_FILE, "r") as f:
        data = f.read()
        try:
            token, chat_id = data.split('\n')[:2]
            bot_id = token.split(':')[0]
            int(bot_id)
            int(chat_id)
            return (token, chat_id)
        except ValueError:
            raise ValueError("Invalid contents in {}, expected token and chat ID".format(CONFIG_FILE))


def send_message(text, config):
    bot = telegram.Bot(token=config[0])
    bot.send_message(chat_id=config[1], text=text, parse_mode=telegram.ParseMode.MARKDOWN_V2)


def main(argv):
    config = load_config()
    argv = argv[1:]

    start = time.time()
    ret = subprocess.call(argv)
    td = str(datetime.timedelta(seconds=int(time.time() - start)))

    msg = "Command `{}` took {} and exited {}".format(
        " ".join(argv), td, "successfully" if ret == 0 else "with an error: {}".format(ret))
    send_message(msg, config)


if __name__ == "__main__":
    main(sys.argv)
