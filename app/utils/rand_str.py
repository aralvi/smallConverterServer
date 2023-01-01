import random
import string


def rand_str(chars=string.ascii_uppercase + string.digits + string.hexdigits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))
