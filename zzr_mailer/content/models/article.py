from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from zzr_mailer.utils.utils import get_img_from_url, trim


class Article(models.Model):
    id = models.CharField(primary_key=True, max_length=63)
    title = models.CharField("Заголовок", max_length=255)
    authors = models.CharField("Авторы", max_length=255, blank=True, null=True)
    teaser = models.TextField("Анонс")
    link = models.URLField("Ссылка")
    header_photo = ProcessedImageField(
        upload_to="img/article/thumbnails",
        processors=[ResizeToFill(600, 360)],
        format="JPEG",
        options={"quality": 90},
        verbose_name="Заглавное изображение",
    )
    header_photo_url = models.URLField(blank=True, null=True)
    year = models.IntegerField("Год публикации", blank=True, null=True)
    issue = models.CharField(
        "Номер выпуска / Код спецвыпуска", max_length=127, blank=True, null=True
    )
    rubric = models.CharField("Рубрика", max_length=127, blank=True, null=True)
    doi = models.CharField("DOI", max_length=127, blank=True, null=True)
    partner = models.CharField("Партнер", max_length=127, blank=True, null=True)
    created = models.DateField("Дата публикации", null=True)

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
