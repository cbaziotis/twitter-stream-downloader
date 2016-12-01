from tweepy import OAuthHandler
from tweepy import Stream

from Listener import Listener

SETTINGS_FILE = "settings.txt"
api_keys_missing = Exception("Twitter API Keys missing! Please fill the API key values in settings.txt ...")


def import_settings():
    _settings = {}

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.startswith("#") or "=" not in line:
                continue
            values = line.split("=")
            key = ' '.join(values[0].split())
            value = ' '.join(values[1].split())
            _settings[key] = value

        _settings["languages"] = [lang.strip() for lang in _settings["languages"].split(",")
                                  if len(_settings["languages"]) > 0]
    return _settings


def validate_twitter_keys(_settings):
    for k, v in _settings.items():
        if k in {"consumer_key", "consumer_secret", "access_token", "access_token_secret"} and not v:
            raise api_keys_missing


if __name__ == '__main__':
    settings = import_settings()
    validate_twitter_keys(settings)
    _listener = Listener(settings["output_folder"],
                         settings["languages"],
                         settings["rt"].lower() == 'true')
    auth = OAuthHandler(settings["consumer_key"], settings["consumer_secret"])
    auth.set_access_token(settings["access_token"], settings["access_token_secret"])

    stream = Stream(auth, _listener, tweet_mode="extended", headers={"tweet_mode": "extended"})
    stream.sample(languages=settings["languages"], async=True)
