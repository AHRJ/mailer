import os
from uuid import uuid4

from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class AdvertisementBanner(models.Model):
    def content_file_name(instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{uuid4()}.{ext}"
        return os.path.join("img/ad/banners", filename)

    title = models.CharField("Заголовок", max_length=255, default="Рекламный баннер")
    image = ProcessedImageField(
        upload_to=content_file_name,
        processors=[ResizeToFill(1200, 720)],
        format="JPEG",
        options={"quality": 95},
        verbose_name="Изображение",
    )
    link = models.URLField("Ссылка")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рекламный баннер"
        verbose_name_plural = "Рекламные баннеры"
