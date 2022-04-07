from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.db import models
from django_q.tasks import async_iter
from pagedown.widgets import AdminPagedownWidget

from zzr_mailer.content.models import Article, Journal
from zzr_mailer.content.news_sources import Zzr

from ..models import IssueAnnouncementLetter
from .abstract_admin import AbstractLetterAdmin


class IssueAnnouncementLetterArticlesLongInline(
    SortableInlineAdminMixin, admin.TabularInline
):
    model = IssueAnnouncementLetter.articles_long.through
    extra = 6


class IssueAnnouncementLetterArticlesShortInline(
    SortableInlineAdminMixin, admin.TabularInline
):
    model = IssueAnnouncementLetter.articles_short.through
    extra = 10


@admin.register(IssueAnnouncementLetter)
class IssueAnnouncementLetterAdmin(AbstractLetterAdmin):

    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }

    inlines = (
        IssueAnnouncementLetterArticlesLongInline,
        IssueAnnouncementLetterArticlesShortInline,
    )

    fields = (
        "journal",
        "title",
        "greeting",
        "advertisement",
        "send_date",
        "addressbooks",
    )

    def add_view(self, request, form_url="", extra_context=None):
        Journal.load_from(Zzr)
        Article.load_from(Zzr)
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        Journal.load_from(Zzr)
        Article.load_from(Zzr)
        return super().change_view(request, object_id, form_url, extra_context)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        articles = [entry for entry in form.instance.articles_long.all()]
        async_iter(Article.fill_header_photo_from_url, articles)
