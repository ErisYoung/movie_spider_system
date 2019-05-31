import datetime
import time


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


if __name__ == '__main__':
    print(get_current_timestamp())
    print(get_current_date())
    print(get_date_from_timestamp(1559093867.101))
    print(get_date_from_timestamp(1559093867.092))

    print(get_timestamp_add(1559093867092))
