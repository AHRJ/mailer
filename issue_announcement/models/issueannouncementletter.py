from django.db import models

from content.models import Article, Journal
from letter.models import Letter

from .advertisement import Advertisement


class IssueAnnouncementLetter(Letter):
    journal = models.ForeignKey(
        Journal, verbose_name="Журнал", on_delete=models.CASCADE
    )
    synopsis = models.TextField("Встуление")
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
        verbose_name = "Рассылочное письмо"
        verbose_name_plural = "Рассылочные письма"


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
