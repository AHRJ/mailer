from django.contrib import admin
from django_object_actions import DjangoObjectActions

from ..models import AddressBook


@admin.register(AddressBook)
class AddressBookAdmin(DjangoObjectActions, admin.ModelAdmin):
    def load_from_dashamail(modeladmin, request, queryset):
        AddressBook.load_from_dashamail()

    load_from_dashamail.label = "Загрузить из Dashamail"

    changelist_actions = ("load_from_dashamail",)
