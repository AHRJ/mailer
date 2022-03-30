from django.db import models

from .letter import Letter


class GenericLetter(Letter):
    letter_type = "genericletter"

    body = models.TextField("Текст письма")

    class Meta:
        verbose_name = "Базовое письмо"
        verbose_name_plural = "Базовые письма"
