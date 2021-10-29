from dataclasses import dataclass
from datetime import datetime

import requests
from django.utils.dateparse import parse_date

from .models import Article, Journal, News


@dataclass
class Zzr:
    BASE_URL = "https://zzr.ru/api/v1"
    NEWS_ENDPOINT = "".join([BASE_URL, "/news"])
    ARTICLE_ENDPOINT = "".join([BASE_URL, "/article"])
    JOURNAL_ENDPOINT = "".join([BASE_URL, "/journal"])

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
        finally:
            return news

    @classmethod
    def get_articles(cls):
        try:
            request = requests.get(cls.ARTICLE_ENDPOINT, timeout=1)
            articles_from_zzr = request.json()
            articles = [
                Article(
                    id=entry["id"],
                    title=entry["title_ru"],
                    authors=entry["authors_ru"],
                    teaser=entry["summary_ru"],
                    link=entry["link"],
                    header_photo_url=entry["header_photo"],
                    year=int(entry["year"]) if entry["year"] else None,
                    issue=entry["issue"],
                    rubric=entry["rubric"],
                    doi=entry["doi"],
                    partner=entry["partner"],
                    created=parse_date(entry["created"]),
                )
                for entry in articles_from_zzr
            ]
        except:  # noqa
            articles = []
        finally:
            return articles

    @classmethod
    def get_journals(cls):
        try:
            request = requests.get(cls.JOURNAL_ENDPOINT, timeout=1)
            journals_from_zzr = request.json()
            journals = [
                Journal(
                    id=entry["id"],
                    link=entry["link"],
                    cover_url=entry["cover"],
                    year=int(entry["year"]) if entry["year"] else None,
                    issue=entry["issue"],
                    created=parse_date(entry["created"]),
                )
                for entry in journals_from_zzr
            ]
        except:  # noqa
            journals = []
        finally:
            return journals
