import io
import uuid
from datetime import datetime

import requests
from django.core.files.images import ImageFile
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel


class News(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    teaser = models.TextField()
    link = models.URLField()
    image = models.ImageField(upload_to="img/news/thumbnails", blank=True)
    image_url = models.URLField(blank=True, null=True)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return " ".join([str(self.pub_date.date()), self.title])

    def load_img_from_url(self):
        if self.image_url and not self.image:
            filename = "".join(["image_", str(self.uuid), ".jpg"])
            image_content = ImageFile(
                io.BytesIO(requests.get(self.image_url).content), name=filename
            )
            self.image = image_content
            self.save()

    @staticmethod
    def load_from_zzr():
        request = requests.get("https://zzr.ru/api/v1/news", timeout=1)
        news_from_zzr = request.json()
        news_to_add = [
            News(
                uuid=entry["uuid"],
                title=entry["title"],
                teaser=entry["teaser"],
                link="".join(["https://zzr.ru", entry["link"]]),
                image_url="".join(["https://zzr.ru", entry["image"]]),
                pub_date=datetime.strptime(entry["pub_date"], "%Y-%m-%d"),
            )
            for entry in news_from_zzr
        ]

        News.objects.bulk_create(news_to_add, ignore_conflicts=True)
        return request.status_code


class Advertisement(models.Model):
    title = models.CharField(max_length=255, default="Рекламный блок")
    body = models.TextField()

    def __str__(self):
        return self.title


class Letter(TimeStampedModel):
    title = models.CharField(max_length=255, default="🐄 Новости животноводства")
    subtitle = models.CharField(max_length=255, default="Актуальные новости отрасли")
    news_long = models.ManyToManyField(
        News, through="LetterNewsLong", related_name="news_long+"
    )
    news_short = models.ManyToManyField(
        News, through="LetterNewsShort", related_name="news_short+"
    )
    advertisement = models.ForeignKey(
        Advertisement, on_delete=models.CASCADE, blank=True, null=True
    )
    send_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return " • ".join([self.title, str(self.pk)])

    @property
    def news_long_sorted(self):
        return self.news_long.order_by("letternewslong__order")

    @property
    def news_short_sorted(self):
        return self.news_short.order_by("letternewsshort__order")


class LetterNewsLong(models.Model):
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order",)


class LetterNewsShort(models.Model):
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order",)
