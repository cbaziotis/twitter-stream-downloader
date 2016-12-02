import ujson as json
from sys import stdout

from tweepy import StreamListener

from EventLogger import EventLogger
from FileManager import FileManager


class Listener(StreamListener):
    """
    A listener handles tweets that are received from the stream.
    """

    def __init__(self, output, languages, save_full, rt, api=None, ):
        super().__init__(api)
        self.logger = EventLogger("tweets")
        self.fmanager = FileManager(output, with_id=not save_full)
        self.languages = languages
        self.save_full = save_full
        self.keep_rt = rt
        print("Downloading...")

    @staticmethod
    def fix_text(text):
        text = ' '.join(text.split())
        return text

    def on_data(self, data):
        tweet = json.loads(data)

        # 1 - Check if there is text in the tweet
        if 'text' not in tweet:
            return True

        # 2 - Check whether to keep the tweet if it is a retweet
        if self.keep_rt or (not self.keep_rt and not tweet['text'].startswith("RT")):

            # 3 - Check whether to save all the tweet or only the text
            if self.save_full:
                self.fmanager.add_entry(data=data)
            else:
                # if the text is longer than 140 chars check if there is available the full_text
                if 'extended_tweet' in tweet and 'full_text' in tweet['extended_tweet']:
                    text = tweet['extended_tweet']['full_text']
                else:
                    text = tweet['text']

                self.fmanager.add_entry(tweet['id_str'], self.fix_text(text))

            self.logger.new_event()

            stdout.write("\r" + self.logger.print_status())
            stdout.flush()
        return True

    def on_error(self, status):
        print(status)
