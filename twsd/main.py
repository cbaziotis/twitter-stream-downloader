import os
import sys

sys.path.append('../')
sys.path.append('./')

import argparse
from argparse import RawTextHelpFormatter
from tweepy import OAuthHandler
from tweepy import Stream

from twsd.Listener import Listener

api_keys_missing = Exception("Twitter API Keys missing! Please fill the "
                             "API key values in settings.txt ... ")


##############################################################################
# Parse Arguments
##############################################################################

def check_empty_arg(value):
    if len(str(value)) == 0:
        raise argparse.ArgumentTypeError("Invalid argument - no value passed.")
    return value


parser = argparse.ArgumentParser(description='twitter stream downloader',
                                 formatter_class=RawTextHelpFormatter)

parser.add_argument('--lang', nargs='?', type=check_empty_arg, default=[],
                    help='filter languages. defaults to no filtering. '
                         'the lang codes must be comma separated.')
parser.add_argument('--storage', nargs='?', type=check_empty_arg,
                    default="text", choices=["text", "db"],
                    help='the type of storage.\n'
                         '- Set to "text" for saving the tweets '
                         'in text files.\n'
                         '- Set to "db" for saving the tweets '
                         'in a MongoDB database.')

parser.add_argument("--omit-rt", help="omit retweets",
                    action="store_true")

parser.add_argument("--only-text", dest='only_text',
                    help="keep only the text. ",
                    action="store_true")

# post-process arguments ###############################
args = parser.parse_args()
args.lang = args.lang.split(',') if args.lang else []


# print(args)


##############################################################################


def import_config():
    _settings = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/settings.txt", "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.startswith("#") or "=" not in line:
                continue
            values = line.split("=")
            key = ' '.join(values[0].split())
            value = ' '.join(values[1].split())
            _settings[key] = value
    return _settings


def validate_twitter_keys(_settings):
    for v in _settings.values():
        if not v:
            raise api_keys_missing


def main():
    config = import_config()
    validate_twitter_keys(config)
    _listener = Listener(args.lang, args.storage, args.only_text, args.omit_rt)
    auth = OAuthHandler(config["consumer_key"],
                        config["consumer_secret"])
    auth.set_access_token(config["access_token"],
                          config["access_token_secret"])

    stream = Stream(auth, _listener, tweet_mode="extended",
                    headers={"tweet_mode": "extended"})
    stream.sample(languages=args.lang, async=True)


if __name__ == '__main__':
    main()
