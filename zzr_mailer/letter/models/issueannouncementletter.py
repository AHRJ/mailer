from django.db import models

from zzr_mailer.content.models import Advertisement, Article, Journal

from .letter import Letter


class IssueAnnouncementLetter(Letter):
    letter_type = "issueannouncementletter"

    journal = models.ForeignKey(
        Journal, verbose_name="Журнал", on_delete=models.CASCADE
    )
    greeting = models.TextField("Приветствие")
    articles_long = models.ManyToManyField(
        Article, through="LetterArticleLong", related_name="article_long+"
    )
    articles_short = models.ManyToManyField(
        Article, through="LetterArticleShort", related_name="article_short+"
    )
    advertisement = models.ForeignKey(
        Advertisement,
        verbose_name="Рекламный блок",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    @property
    def articles_long_sorted(self):
        return self.articles_long.order_by("letterarticlelong__order")

    @property
    def articles_short_sorted(self):
        return self.articles_short.order_by("letterarticleshort__order")

    class Meta:
        verbose_name = "Анонс журнала"
        verbose_name_plural = "Анонсы журнала"


class LetterArticleLong(models.Model):
    letter = models.ForeignKey(IssueAnnouncementLetter, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order",)
        verbose_name = "Статья с анонсом"
        verbose_name_plural = "Статьи с анонсом"


class LetterArticleShort(models.Model):
    letter = models.ForeignKey(IssueAnnouncementLetter, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order",)
        verbose_name = "Другая статья"
        verbose_name_plural = "Другие статьи"
