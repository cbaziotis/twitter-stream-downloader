import ujson as json
from sys import stdout

from tweepy import StreamListener

from twsd.EventLogger import EventLogger
from twsd.StorageManager import FileManager, DatabaseManager


class Listener(StreamListener):
    """
    A listener handles tweets that are received from the stream.
    """

    def __init__(self, languages, storage, only_text, omit_rt, api=None):
        super().__init__(api)
        self.logger = EventLogger("tweets")

        if storage == "text":
            self.storage = FileManager(only_text)
        elif storage == "db":
            self.storage = DatabaseManager(only_text)

        self.languages = languages
        self.only_text = only_text
        self.omit_rt = omit_rt
        print("Downloading...")

    def on_data(self, data):
        tweet = json.loads(data)

        # 1 - Check if there is text in the tweet
        if 'text' not in tweet:
            return True

        # 2 - Check whether to keep the tweet if it is a retweet
        if tweet['text'].startswith("RT") and self.omit_rt:
            return True

        self.storage.save(tweet, data)

        self.logger.new_event()

        stdout.write("\r" + self.logger.print_status())
        stdout.flush()

        return True

    def on_error(self, status):
        print(status)
