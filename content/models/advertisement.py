from django.db import models


class Advertisement(models.Model):
    title = models.CharField(max_length=255, default="Рекламный блок")
    body = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Рекламный блок"
        verbose_name_plural = "Рекламные блоки"
