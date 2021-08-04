from datetime import timedelta

from django.utils import timezone


def trim(string):
    return "".join([string[:75], "..."]) if len(string) > 75 else string


def next_monday():
    current_date = timezone.now().replace(hour=10, minute=0, second=0)
    monday = 0
    return current_date + timedelta(days=(monday - current_date.weekday() + 7) % 7)
