class TimeConvertor:
    def __init__(self, start_value, duration):
        self.start_value = start_value
        self.duration = duration

    @property
    def convert_start_time(self):
        hours = int(self.start_value / 3600)
        minutes = int((self.start_value % 3600) / 60)
        seconds = int((self.start_value % 3600) % 60)
        milliseconds = int((self.start_value % 1.0) * 1000)
        start_time = "{:02d}:{:02d}:{:02d},{:03d}".format(int(hours), int(minutes), int(seconds),
                                                          int(milliseconds))
        return start_time

    @property
    def convert_end_time(self):
        end_value = self.start_value + self.duration
        hours = int(end_value / 3600)
        minutes = int((end_value % 3600) / 60)
        seconds = int((end_value % 3600) % 60)
        milliseconds = int((end_value % 1.0) * 1000)
        end_time = "{:02d}:{:02d}:{:02d},{:03d}".format(int(hours), int(minutes), int(seconds),
                                                        int(milliseconds))
        return end_time
