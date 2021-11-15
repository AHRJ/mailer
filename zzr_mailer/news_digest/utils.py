import io
from datetime import timedelta

import requests
from django.core.files.images import ImageFile
from django.utils import timezone


def trim(string):
    return "".join([string[:75], "..."]) if len(string) > 75 else string


def next_monday():
    current_date = timezone.now().replace(hour=10, minute=0, second=0)
    monday = 0
    return current_date + timedelta(days=(monday - current_date.weekday() + 7) % 7)


def get_img_from_url(url, filename):
    try:
        img = ImageFile(io.BytesIO(requests.get(url).content), name=filename)
    except:  # noqa
        img = None
    return img
