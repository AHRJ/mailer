import uuid

from django.db import models
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from model_utils.models import TimeStampedModel

from news_digest.utils import get_img_from_url, trim


class News(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    teaser = models.TextField()
    link = models.URLField()
    image = ProcessedImageField(
        upload_to="img/news/thumbnails",
        processors=[ResizeToFill(300, 180)],
        format="JPEG",
        options={"quality": 90},
    )
    image_url = models.URLField(blank=True, null=True)
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        date = str(self.pub_date.date())
        short_title = trim(self.title)
        return " ".join([date, short_title])

    def fill_img_from_url(self):
        if self.image_url and not self.image:
            filename = "".join(["image_", str(self.uuid), ".jpg"])
            self.image = get_img_from_url(self.image_url, filename)
            self.save()

    @staticmethod
    def load_from(source):
        News.objects.bulk_create(source.get_news(), ignore_conflicts=True)
