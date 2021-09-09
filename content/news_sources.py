from datetime import datetime

import requests

from .models import News


class Zzr:
    def __init__(self):
        pass

    @staticmethod
    def get_news():
        try:
            request = requests.get("https://zzr.ru/api/v1/news", timeout=1)
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
        finally:
            return news
