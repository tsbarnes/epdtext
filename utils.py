from settings import DEBUG


def log(message):
    if DEBUG:
        print(message)
