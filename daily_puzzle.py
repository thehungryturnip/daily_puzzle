#!/usr/bin/env python3

import sys
from datetime import date

WEEKDAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')


if len(sys.argv) > 1:
    today = date.fromisoformat(sys.argv[1])
else:
    today = date.today()
print(f'{today} {WEEKDAYS[today.weekday()]}')
