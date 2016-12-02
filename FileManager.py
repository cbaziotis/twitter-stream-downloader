import datetime
import os
import threading


class FileManager:
    def __init__(self, directory="dump", with_id=True):
        self.directory = directory

        # whether to save the tweet_id with data or not, useful for deduplication
        self.with_id = with_id
        self.buffer = []

        # the size of the buffer.
        # if the buffer reaches it's limit then it's contents will be written to disk
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
        return "_".join(["{0:0>2}".format(v) for v in [now.year, now.month, now.day, now.hour]])

    def init_check(self):
        """
        Check if the output folder contains any files, and if so resume without overwriting the old
        :return:
        """
        self.assure_path_exists(self.directory)

    def add_entry(self, _id=None, data=None):
        """
        Add a new entry in the output file
        :param _id:
        :param data:
        :return:
        """
        if self.with_id:
            self.buffer.append((_id, data))
        else:
            self.buffer.append(data)

        # if buffer is "full" then write the contents to disk
        if len(self.buffer) >= self.buffer_limit:
            # execute the file write in a new thread
            threading.Thread(daemon=True, target=self.write_data, args=(self.buffer[:],)).start()
            self.buffer[:] = []  # empty the buffer

    def write_data(self, data):
        """
        Write the buffer  to the output file
        :return:
        """
        filename = self.get_filename() + ".tsv"
        path = os.path.join(self.directory, filename)
        with open(path, mode="a", encoding="utf-8") as f:
            if self.with_id:
                for entry in data:
                    f.write("\t".join(entry) + "\n")
            else:
                for entry in data:
                    f.write(entry.rstrip() + "\n")
