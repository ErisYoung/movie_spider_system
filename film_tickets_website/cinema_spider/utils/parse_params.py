import datetime


def get_current_timestamp():
    now = datetime.datetime.now()
    timestamp_str = f"{int(now.timestamp()*1000)}"
    return timestamp_str


def get_current_date():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    return date_str


if __name__ == '__main__':
    print(get_current_timestamp())
    print(get_current_date())
