from datetime import datetime, time, timedelta
import time
import humanize

class Humanize(object):

    @staticmethod
    def trasnform(timestamp):
        ts = time.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        d2 = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        d2 = datetime.strptime(d2, '%Y-%m-%d %H:%M:%S')
        return humanize.naturaltime(d2 - timedelta(hours=3))