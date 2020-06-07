import sys
import os
import time
import json
import urllib.request
import datetime
import subprocess


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
    data = {
        "text": text,
        "chat_id": config[1],
        "parse_mode": "MarkdownV2",
        "disable_notification": True
    }
    req = urllib.request.Request("https://api.telegram.org/bot{}/sendMessage".format(config[0]),
                                 bytes(json.dumps(data), encoding="utf-8"),
                                 {"Content-Type": "application/json"})
    urllib.request.urlopen(req)


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
