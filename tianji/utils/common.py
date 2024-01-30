from datetime import datetime


def timestamp_str():
    now = datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    timestamp_str = (
        timestamp_str[:-3]
        .replace(" ", "_")
        .replace(":", "")
        .replace("-", "")
        .replace(".", "")
    )
    return timestamp_str
