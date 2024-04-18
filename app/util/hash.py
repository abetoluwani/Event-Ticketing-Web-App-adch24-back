#!/usr/bin/env python3
# File: hash.py
# Author: Oluwatobiloba Light
"""Hash"""

import uuid


def get_rand_hash(length=16):
    return uuid.uuid4().hex[:length]
