#!/usr/bin/env python3
# File: date.py
# Author: Oluwatobiloba Light
"""Date module"""

from datetime import datetime

from pytz import timezone


def get_now():
    return datetime.now(tz=timezone("UTC"))
