import datetime


def date_time():
    e = datetime.datetime.now()

    date = "{}-{}-{}".format(e.day, e.month, e.year)
    time = "{}:{}:{}".format(e.hour, e.minute, e.second)

    print("Date: {}  Time: {}".format(date, time))
