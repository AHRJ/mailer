import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from model_utils.models import TimeStampedModel

from .utils import get_img_from_url, next_monday, trim


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

    def __str__(self):
        date = str(self.pub_date.date())
        short_title = trim(self.title)
        return " ".join([date, short_title])

    def fill_img_from_url(self):
        if self.image_url and not self.image:
            filename = "".join(["image_", str(self.uuid), ".jpg"])
            self.image = get_img_from_url(self.image_url, filename)
            self.save()

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    @staticmethod
    def load_from(source):
        News.objects.bulk_create(source.get_news(), ignore_conflicts=True)


class Advertisement(models.Model):
    title = models.CharField(max_length=255, default="Рекламный блок")
    body = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рекламный блок"
        verbose_name_plural = "Рекламные блоки"


class AddressBook(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255, default="Адресная книга")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Адресная книга"
        verbose_name_plural = "Адресные книги"


class Campaign(models.Model):
    id = models.PositiveIntegerField(primary_key=True)


class Letter(TimeStampedModel):
    class Status(models.TextChoices):
        UNPLANNED = "UNP", "Не запланирована"
        PENDING = "PND", "Обработка..."
        PLANNED = "PLA", "Запланирована"
        SENT = "SNT", "Отправлена"
        EXPIRED = "EXP", "Просрочена"
        ERROR = "ERR", "Ошибка"

    title = models.CharField(
        "Тема письма", max_length=255, default="🐄 Новости животноводства"
    )
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
    campaigns = models.ManyToManyField(Campaign, blank=True)
    addressbooks = models.ManyToManyField(
        AddressBook,
        blank=True,
        default=AddressBook.objects.all,
        verbose_name="Адресные книги",
    )
    send_date = models.DateTimeField(default=next_monday, verbose_name="Дата отправки")
    status = models.CharField(
        max_length=3,
        choices=Status.choices,
        default=Status.UNPLANNED,
        verbose_name="Статус",
    )

    def __str__(self):
        return " • ".join([self.title, str(self.pk)])

    def clean(self):
        if self.send_date < timezone.now():
            raise ValidationError("Дата отправки не может быть меньше текущей")

    def update_status(self):
        if self.status == Letter.Status.PENDING or self.status == Letter.Status.ERROR:
            pass
        elif self.send_date > timezone.now() and not self.campaigns.exists():
            self.status = Letter.Status.UNPLANNED
        elif self.send_date > timezone.now() and self.campaigns.exists():
            self.status = Letter.Status.PLANNED
        elif self.send_date < timezone.now() and self.campaigns.exists():
            self.status = Letter.Status.SENT
        elif self.send_date < timezone.now() and not self.campaigns.exists():
            self.status = Letter.Status.EXPIRED
        self.save()

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
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order",)
        verbose_name = "Новость с анонсом"
        verbose_name_plural = "Новости с анонсом"


class LetterNewsShort(models.Model):
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order",)
        verbose_name = "Новость 'Одной строкой'"
        verbose_name_plural = "Новости 'Одной строкой'"
