from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django_q.tasks import async_iter

from zzr_mailer.content.models import News
from zzr_mailer.content.news_sources import Zzr

from .models import NewsDigestLetter


class NewsDigestLetterNewsLongInline(SortableInlineAdminMixin, admin.TabularInline):
    model = NewsDigestLetter.news_long.through
    extra = 8


class NewsDigestLetterNewsShortInline(SortableInlineAdminMixin, admin.TabularInline):
    model = NewsDigestLetter.news_short.through
    extra = 10


@admin.register(NewsDigestLetter)
class NewsDigestLetterAdmin(admin.ModelAdmin):
    inlines = (
        NewsDigestLetterNewsLongInline,
        NewsDigestLetterNewsShortInline,
    )
    list_display = (
        "title",
        "send_date",
        "detail_view",
        "status",
        "create_campaign",
    )

    fields = (
        "title",
        "subtitle",
        "advertisement",
        "send_date",
        "addressbooks",
    )

    def detail_view(self, obj):
        url = reverse("news_digest:detail", args=[obj.id])
        return format_html(f"<a href='{url}'>Просмотр</a>")

    detail_view.short_description = "Ссылка"

    def create_campaign(self, obj):
        obj.update_status()

        if obj.status == NewsDigestLetter.Status.UNPLANNED:
            url = reverse("news_digest:create_campaign", args=[obj.id])
            text = "Запланировать рассылку"
        elif obj.status == NewsDigestLetter.Status.PENDING:
            url = "#"
            text = ""
        elif obj.status == NewsDigestLetter.Status.SENT:
            url = "#"
            text = ""
        elif obj.status == NewsDigestLetter.Status.PLANNED:
            url = reverse("news_digest:cancel_campaign", args=[obj.id])
            text = "Отменить рассылку"
        elif obj.status == NewsDigestLetter.Status.EXPIRED:
            url = ""
            text = ""
        elif obj.status == NewsDigestLetter.Status.ERROR:
            url = ""
            text = ""
        return format_html(f"<a href='{url}'>{text}</a>")

    create_campaign.short_description = "Действия"

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