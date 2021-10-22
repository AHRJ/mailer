from django.db import models


class AddressBook(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255, default="Адресная книга")
    status = models.BooleanField(verbose_name="Активная", default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Адресная книга"
        verbose_name_plural = "Адресные книги"
