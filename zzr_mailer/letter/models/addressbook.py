from django.db import models

from zzr_mailer.utils.dashamail import Dashamail


class AddressBook(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255, default="Адресная книга")
    is_active = models.BooleanField(verbose_name="Активная", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Адресная книга"
        verbose_name_plural = "Адресные книги"

    @staticmethod
    def load_from_dashamail():
        try:
            addressbooks_from_dashamail = Dashamail.get_list_of_addressbooks()
            addressbooks = [
                AddressBook(id=addressbook["id"], name=addressbook["name"])
                for addressbook in addressbooks_from_dashamail
            ]
            addressbook_ids = [
                addressbook["id"] for addressbook in addressbooks_from_dashamail
            ]
        except:  # noqa
            addressbooks = []

        AddressBook.objects.bulk_create(addressbooks, ignore_conflicts=True)
        AddressBook.objects.exclude(
            id__in=addressbook_ids
        ).delete()  # rm nonexistent adressbooks
