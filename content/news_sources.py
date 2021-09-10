from dataclasses import dataclass
from datetime import datetime

import requests

from .models import News


@dataclass
class Zzr:
    BASE_URL = "https://zzr.ru/api/v1"
    NEWS_ENDPOINT = "".join([BASE_URL, "/news"])

    @classmethod
    def get_news(cls):
        try:
            request = requests.get(cls.NEWS_ENDPOINT, timeout=1)
            news_from_zzr = request.json()
            news = [
                News(
                    uuid=entry["uuid"],
                    title=entry["title"],
                    teaser=entry["teaser"],
                    link=entry["link"],
                    image_url=entry["image"],
                    pub_date=datetime.strptime(entry["pub_date"], "%Y-%m-%d"),
                )
                for entry in news_from_zzr
            ]
        except:  # noqa
            news = []
            raise
        finally:
            return news
