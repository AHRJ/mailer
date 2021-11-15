from django.contrib import admin
from django_object_actions import DjangoObjectActions

from .models import AddressBook


@admin.register(AddressBook)
class AddressBookAdmin(DjangoObjectActions, admin.ModelAdmin):
    def load_from_sendpulse(modeladmin, request, queryset):
        AddressBook.load_from_sendpulse()

    load_from_sendpulse.label = "Загрузить из Sendpulse"

    changelist_actions = ("load_from_sendpulse",)
