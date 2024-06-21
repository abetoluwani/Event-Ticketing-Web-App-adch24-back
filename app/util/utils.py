#!/usr/bin/env python3
# File: utils.py
# Author: Oluwatobiloba Light
"""Utils module"""


from collections import namedtuple
from datetime import datetime, timedelta, timezone
from typing import Any


def get_remaining_minutes(user_info: Any) -> float:
    """"""
    current_time_stamp = user_info['exp']

    system_tz_offset = timezone(timedelta(hours=1))

    # Get current time in system time zone (naive object)
    local_time = datetime.now()

    # Convert local time to UTC (considering system time zone offset)
    current_utc_time = local_time.astimezone(system_tz_offset).timestamp()

    time_delta = timedelta(seconds=current_time_stamp - int(current_utc_time))

    remaining_minutes = time_delta.total_seconds() / 60

    return remaining_minutes


def create_named_tuple(*values):
    return namedtuple('NamedTuple', values)(*values)
