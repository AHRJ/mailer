from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel

from news_digest.utils import next_monday

from .addressbook import AddressBook
from .campaign import Campaign


def get_all_addressbooks():
    return AddressBook.objects.all()


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
    campaigns = models.ManyToManyField(Campaign, blank=True)
    addressbooks = models.ManyToManyField(
        AddressBook,
        blank=True,
        default=get_all_addressbooks,
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

    class Meta:
        abstract = True
