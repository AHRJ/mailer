from django.contrib import admin

from zzr_mailer.content.models import Journal
from zzr_mailer.content.news_sources import Zzr

from ..models import IssueDownloadLetter
from .abstract_admin import AbstractLetterAdmin


@admin.register(IssueDownloadLetter)
class IssueDownloadLetterAdmin(AbstractLetterAdmin):

    fields = (
        "journal",
        "send_date",
        "addressbooks",
    )

    def add_view(self, request, form_url="", extra_context=None):
        Journal.load_from(Zzr)
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        Journal.load_from(Zzr)
        return super().change_view(request, object_id, form_url, extra_context)
