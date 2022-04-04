from django.db import models

from .letter import Letter


class GenericLetter(Letter):
    letter_type = "genericletter"

    body = models.TextField("Текст письма")

    class Meta:
        verbose_name = "Обычное письмо"
        verbose_name_plural = "Обычные письма"
