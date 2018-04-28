from datetime import datetime


def print_message(message):
    print(datetime.now().isoformat(), message)
    return message