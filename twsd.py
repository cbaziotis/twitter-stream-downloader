import argparse

from tweepy import OAuthHandler
from tweepy import Stream

from Listener import Listener

SETTINGS_FILE = "settings.txt"
api_keys_missing = Exception("Twitter API Keys missing! Please fill the API key values in settings.txt ... ")


##############################################################################################################
# Parse Arguments
##############################################################################################################

def check_empty_arg(value):
    if len(str(value)) == 0:
        raise argparse.ArgumentTypeError("Invalid argument - no value passed.")
    return value


parser = argparse.ArgumentParser()

# add arguments ########################################
parser.add_argument('--lang', nargs='?', type=check_empty_arg, default=[],
                    help='filter languages. defaults to no filtering. the lang codes must be comma separated.')
parser.add_argument('--output', nargs='?', type=check_empty_arg, default="dump",
                    help='the name of the folder where the twitter data will be saved.')

# save retweets or not
feature_parser = parser.add_mutually_exclusive_group()
# feature_parser.add_argument('--rt', dest='rt', action='store_true', help='save retweets.')
feature_parser.add_argument('--no-rt', dest='save_rt', action='store_false', help="dont't save retweets.")
parser.set_defaults(save_rt=True)

# keep all the twitter data or only the text
feature_parser = parser.add_mutually_exclusive_group()
# feature_parser.add_argument('--keep-all', dest='keep_mode', action='store_true', help='keep all the twitter data')
feature_parser.add_argument('--only-text', dest='save_full', action='store_false', help="keep only the text")
parser.set_defaults(save_full=True)

# post-process arguments ###############################
args = parser.parse_args()
args.lang = args.lang.split(',') if args.lang else []


# print(args)


##############################################################################################################


def import_config():
    _settings = {}

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
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
    _listener = Listener(args.output, args.lang, args.save_full, args.save_rt)
    auth = OAuthHandler(config["consumer_key"], config["consumer_secret"])
    auth.set_access_token(config["access_token"], config["access_token_secret"])

    stream = Stream(auth, _listener, tweet_mode="extended", headers={"tweet_mode": "extended"})
    stream.sample(languages=args.lang, async=True)


if __name__ == '__main__':
    main()
