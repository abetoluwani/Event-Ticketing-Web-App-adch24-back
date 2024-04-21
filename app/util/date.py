#!/usr/bin/env python3
# File: date.py
# Author: Oluwatobiloba Light
"""Date module"""

from datetime import datetime, time
from typing import Optional

from pytz import timezone


def get_now():
    return datetime.now(tz=timezone("UTC"))


def get_am_pm(t):
  """
  This function takes a datetime.time object and returns "AM" or "PM"
  depending on the hour.
  """
  hour = t.hour
  return "PM" if hour >= 12 else "AM"


def format_time_with_am_pm(t: Optional[time]) -> Optional[str]:
  """
  This function takes an optional datetime.time object and returns a
  formatted string with AM/PM.
  """
  from time import time
  if not t:
      return None

  return f"{t} {get_am_pm(t)}"
