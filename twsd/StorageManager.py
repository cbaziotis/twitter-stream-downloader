import datetime
import os
import threading

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class StorageManager:
    def __init__(self, only_text):
        self.only_text = only_text

    def add_entry(self, _id, data, str_data):
        pass

    @staticmethod
    def fix_text(text):
        text = text.replace('\n', '')
        text = ' '.join(text.split(' '))
        return text

    def extract_text(self, data):
        if 'extended_tweet' in data and 'full_text' in data['extended_tweet']:
            text = data['extended_tweet']['full_text']
        else:
            text = data['text']
        text = self.fix_text(text)
        return text

    def save(self, data, str_data):
        _id = data['id_str']
        self.add_entry(_id, data, str_data)


class DatabaseManager(StorageManager):
    def __init__(self, only_text):
        super().__init__(only_text)

        self.client = MongoClient()
        self.db = self.client.twsd_database
        self.tweets = self.db.tweets
        self.duplicates = 0

    def get_entry(self, _id, data):
        if self.only_text:
            return {"_id": _id, "text": self.extract_text(data)}
        else:
            data["_id"] = _id
            return data

    def add_entry(self, _id, data, str_data):
        entry = self.get_entry(_id, data)
        try:
            self.tweets.insert_one(entry)
        except DuplicateKeyError:
            self.duplicates += 1
            if self.duplicates % 100 == 0:
                print()
                print("duplicates: {}".format(self.duplicates))


class FileManager(StorageManager):
    def __init__(self, only_text, directory="output"):
        super().__init__(only_text)

        self.directory = directory

        # whether to save the tweet_id with data or not,
        # useful for deduplication
        self.buffer = []

        # the size of the buffer. if the buffer reaches it's limit
        # then it's contents will be written to disk
        self.buffer_limit = 100

        self.init_check()

    @staticmethod
    def assure_path_exists(path):
        _dir = os.path.join(path)
        if not os.path.exists(_dir):
            os.makedirs(_dir)

    @staticmethod
    def get_filename():
        now = datetime.datetime.now()
        return "_".join(["{0:0>2}".format(v) for v in
                         [now.year, now.month, now.day, now.hour]])

    def init_check(self):
        """
        Check if the output folder contains any files, and if so resume without overwriting the old
        """
        self.assure_path_exists(self.directory)

    def update_buffer(self):
        # if buffer is "full" then write the contents to disk
        # todo: show count of threads
        if len(self.buffer) >= self.buffer_limit:
            # execute the file write in a new thread
            threading.Thread(daemon=True, target=self.write_data,
                             args=(self.buffer[:],)).start()
            self.buffer[:] = []  # empty the buffer

    def add_entry(self, _id, data, str_data):
        """
        Add a new entry in the output file
        """
        if self.only_text:
            entry = self.extract_text(data)
            self.buffer.append((_id, entry))
        else:
            self.buffer.append(str_data)

        self.update_buffer()

    def write_data(self, data):
        """
        Write the buffer  to the output file
        :return:
        """
        filename = self.get_filename() + ".tsv"
        path = os.path.join(self.directory, filename)
        with open(path, mode="a", encoding="utf-8") as f:
            for entry in data:
                if self.only_text:
                    f.write("\t".join(entry) + "\n")
                else:
                    f.write(entry.rstrip() + "\n")
