import random
from werkzeug.security import gen_salt


def generate_csrf():
    length = random.randint(1, 11) * 3
    return gen_salt(length)
