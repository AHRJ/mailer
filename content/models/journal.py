from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from news_digest.utils import get_img_from_url


class Journal(models.Model):
    id = models.CharField(primary_key=True, max_length=63)
    issue = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    link = models.URLField()
    cover = ProcessedImageField(
        upload_to="img/journal/thumbnails",
        processors=[ResizeToFill(600, 360)],
        format="JPEG",
        options={"quality": 90},
    )
    cover_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Журнал"
        verbose_name_plural = "Журналы"

    def __str__(self):
        return " ".join(["Животноводство России - ", self.issue, str(self.year)])

    def fill_cover_from_url(self):
        if self.cover and not self.cover_url:
            filename = "".join([str(self.id), ".jpg"])
            self.cover = get_img_from_url(self.cover_url, filename)
            self.save()

    @staticmethod
    def load_from(source):
        Journal.objects.bulk_create(source.get_journals(), ignore_conflicts=True)
