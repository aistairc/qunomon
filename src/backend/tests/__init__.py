# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from qai_testbed_backend import create_app
import random
import string

app = create_app('testing', True)


def get_random_str(n: int):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))
