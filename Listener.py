
from sys import stdout

from tweepy import StreamListener

from EventLogger import EventLogger
from FileManager import FileManager
import ujson as json


class Listener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self,  output, languages, rt, api=None, ):
        super().__init__(api)
        self.roe = EventLogger("tweets")
        self.fm = FileManager(output)
        self.languages = languages
        self.rt = rt
        print("Downloading...")

    @staticmethod
    def fix_text(text):
        text = ' '.join(text.split())
        return text

    def on_data(self, data):
        tweet = json.loads(data)
        skip_rt = not self.rt and tweet['text'].startswith("RT")
        if 'text' in tweet and not skip_rt:

            tweet_id = tweet['id_str']

            # if the text is longer than 140 chars check if there is available the full_text
            if 'extended_tweet' in tweet and 'full_text' in tweet['extended_tweet']:
                text = tweet['extended_tweet']['full_text']
            else:
                text = tweet['text']

            text = self.fix_text(text)
            # print(text)

            self.fm.add_entry(tweet_id, text)

            self.roe.new_event()
            stdout.write("\r" + self.roe.print_status())
            stdout.flush()
        return True

    def on_error(self, status):
        print(status)
