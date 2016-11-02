import random


def shuffle_string(message='0123456789'):
    # return (''.join(random.sample(message, len(message))))
    return (lambda s:''.join(random.sample(s, len(s))))(message)


if __name__ == "__main__":
    shuffle_string()

