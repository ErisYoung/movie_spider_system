import datetime
import time

MTIME_TIME_LENGTH = 16


def get_current_timestamp():
    now = datetime.datetime.now()
    timestamp_str = f"{int(now.timestamp()*1000)}"
    return timestamp_str


def get_timestamp_add(timestamp):
    return str(int(timestamp) + 9)


def get_date_from_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def get_current_date():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    return date_str


def get_current_date_str():
    now = datetime.datetime.now()
    time_tuple = now.timetuple()
    format_string = f"{time_tuple.tm_year}{time_tuple.tm_mon}{time_tuple.tm_mday}{time_tuple.tm_hour}{time_tuple.tm_min}{time_tuple.tm_sec}"
    format_string += (MTIME_TIME_LENGTH - len(format_string)) * "0"
    return format_string


if __name__ == '__main__':
    print(get_current_timestamp())
    print(get_current_date())
    print(get_date_from_timestamp(1559093867.101))
    print(get_date_from_timestamp(1559093867.092))
    print(get_timestamp_add(1559093867092))
    print(get_current_date_str())
