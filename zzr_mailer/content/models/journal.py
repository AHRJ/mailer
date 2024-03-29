import os
from uuid import uuid4

from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from zzr_mailer.utils.utils import get_img_from_url


class Journal(models.Model):
    class IssueType(models.TextChoices):
        REGULAR = "R", "Номерной"
        SPECIAL = "S", "Тематический"

    def content_file_name(instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{instance.pk}-{uuid4().hex[0:7]}.{ext}"
        return os.path.join("files/journal/pdf", filename)

    id = models.CharField(primary_key=True, max_length=63)
    issue = models.CharField("Номер выпуска / Код спецвыпуска", max_length=255)
    issue_type = models.CharField(
        max_length=1,
        choices=IssueType.choices,
        default=IssueType.REGULAR,
        verbose_name="Тип выпуска",
    )
    year = models.IntegerField("Год", blank=True, null=True)
    link = models.URLField("Ссылка")
    cover = ProcessedImageField(
        upload_to="img/journal/thumbnails",
        processors=[ResizeToFill(320, 442)],
        format="JPEG",
        options={"quality": 90},
        verbose_name="Обложка",
    )
    cover_url = models.URLField(blank=True, null=True)
    created = models.DateField("Дата размещения", null=True)
    pdf = models.FileField(verbose_name="PDF", upload_to=content_file_name, blank=True)

    class Meta:
        verbose_name = "Журнал"
        verbose_name_plural = "Журналы"

    def __str__(self):
        return " ".join(["Животноводство России - ", self.issue, str(self.year)])

    def save(self, *args, **kwargs):
        issue_type = self.id.split("-")[2]
        if issue_type in ["PT", "SV", "SK"]:
            self.issue_type = self.IssueType.SPECIAL
        super(Journal, self).save(*args, **kwargs)

    def fill_cover_from_url(self):
        if self.cover_url and not self.cover:
            filename = "".join([str(self.id), ".jpg"])
            self.cover = get_img_from_url(self.cover_url, filename)
            self.save()

    @staticmethod
    def load_from(source):
        Journal.objects.bulk_create(source.get_journals(), ignore_conflicts=True)
        [journal.fill_cover_from_url() for journal in Journal.objects.all()]
