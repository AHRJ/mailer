from django.db import models

from zzr_mailer.content.models import Advertisement, News
from zzr_mailer.letter.models import Letter


class NewsDigestLetter(Letter):
    subtitle = models.CharField(
        "Заголовок письма", max_length=255, default="Актуальные новости отрасли"
    )
    news_long = models.ManyToManyField(
        News, through="LetterNewsLong", related_name="news_long+"
    )
    news_short = models.ManyToManyField(
        News, through="LetterNewsShort", related_name="news_short+"
    )
    advertisement = models.ForeignKey(
        Advertisement,
        verbose_name="Рекламный блок",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    @property
    def news_long_sorted(self):
        return self.news_long.order_by("letternewslong__order")

    @property
    def news_short_sorted(self):
        return self.news_short.order_by("letternewsshort__order")

    class Meta:
        verbose_name = "Рассылочное письмо"
        verbose_name_plural = "Рассылочные письма"


class LetterNewsLong(models.Model):
    letter = models.ForeignKey(NewsDigestLetter, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order",)
        verbose_name = "Новость с анонсом"
        verbose_name_plural = "Новости с анонсом"


class LetterNewsShort(models.Model):
    letter = models.ForeignKey(NewsDigestLetter, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order",)
        verbose_name = "Новость 'Одной строкой'"
        verbose_name_plural = "Новости 'Одной строкой'"
