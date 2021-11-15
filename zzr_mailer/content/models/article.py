from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from zzr_mailer.news_digest.utils import get_img_from_url, trim


class Article(models.Model):
    id = models.CharField(primary_key=True, max_length=63)
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255, blank=True, null=True)
    teaser = models.TextField()
    link = models.URLField()
    header_photo = ProcessedImageField(
        upload_to="img/article/thumbnails",
        processors=[ResizeToFill(600, 360)],
        format="JPEG",
        options={"quality": 90},
    )
    header_photo_url = models.URLField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    issue = models.CharField(max_length=127, blank=True, null=True)
    rubric = models.CharField(max_length=127, blank=True, null=True)
    doi = models.CharField(max_length=127, blank=True, null=True)
    partner = models.CharField(max_length=127, blank=True, null=True)
    created = models.DateField(null=True)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        short_title = trim(self.title)
        return short_title

    def fill_header_photo_from_url(self):
        if self.header_photo_url and not self.header_photo:
            filename = "".join(["image_", str(self.id), ".jpg"])
            self.header_photo = get_img_from_url(self.header_photo_url, filename)
            self.save()

    @staticmethod
    def load_from(source):
        Article.objects.bulk_create(source.get_articles(), ignore_conflicts=True)
