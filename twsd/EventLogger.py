import datetime as dt


class EventLogger:
    def __init__(self, event_name=None):
        self.event_name = event_name or "events"
        self.diffs = []
        self.last_time = dt.datetime.today().timestamp()
        self.total = 0
        self.init_time = dt.datetime.today().timestamp()
        self.rate_sample_size = 20

    @staticmethod
    def format_time(secs):
        m, s = divmod(secs, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    @staticmethod
    def human_format_number(num):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        # add more suffixes if you need them
        return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

    def new_event(self):
        self.total += 1

        new_time = dt.datetime.today().timestamp()
        self.diffs.append(new_time - self.last_time)
        self.last_time = new_time

        # Clip the list
        if len(self.diffs) > self.rate_sample_size:
            self.diffs = self.diffs[-self.rate_sample_size:]

    def get_rate(self):
        try:
            return len(self.diffs) / sum(self.diffs)
        except:
            return 0

    def get_total(self):
        return self.total

    def get_total_time(self):
        tt = dt.datetime.today().timestamp() - self.init_time
        return self.format_time(tt)

    def get_total_events(self):
        return self.human_format_number(self.total)

    def print_status(self):
        message = "Total: %5s \t Rate: %5.2f %s/sec \t time: %s"
        return message % (self.total,
                          self.get_rate(),
                          self.event_name,
                          self.get_total_time())
