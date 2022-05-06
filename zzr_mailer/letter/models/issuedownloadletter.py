from django.db import models

from zzr_mailer.content.models import Journal

from .letter import Letter


class IssueDownloadLetter(Letter):
    letter_type = "issuedownloadletter"

    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Выпуск журнала подписчикам"
        verbose_name_plural = "Выпуски журнала подписчикам"

    def save(self, *args, **kwargs):
        title = f"Ваш PDF журнала «Животноводство России». {self.journal.issue} {self.journal.year}"
        self.title = title
        super().save(*args, **kwargs)
