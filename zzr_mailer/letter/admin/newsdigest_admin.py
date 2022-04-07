from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django_q.tasks import async_iter

from zzr_mailer.content.models import News
from zzr_mailer.content.news_sources import Zzr

from ..models import NewsDigestLetter
from .abstract_admin import AbstractLetterAdmin


class NewsDigestLetterNewsLongInline(SortableInlineAdminMixin, admin.TabularInline):
    model = NewsDigestLetter.news_long.through
    extra = 8


class NewsDigestLetterNewsShortInline(SortableInlineAdminMixin, admin.TabularInline):
    model = NewsDigestLetter.news_short.through
    extra = 10


@admin.register(NewsDigestLetter)
class NewsDigestLetterAdmin(AbstractLetterAdmin):
    inlines = (
        NewsDigestLetterNewsLongInline,
        NewsDigestLetterNewsShortInline,
    )

    fields = (
        "title",
        "subtitle",
        "advertisement",
        "send_date",
        "addressbooks",
    )

    def add_view(self, request, form_url="", extra_context=None):
        News.load_from(Zzr)
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        News.load_from(Zzr)
        return super().change_view(request, object_id, form_url, extra_context)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        news = [entry for entry in form.instance.news_long.all()]
        async_iter(News.fill_img_from_url, news)
