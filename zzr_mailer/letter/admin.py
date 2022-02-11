from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django_object_actions import DjangoObjectActions
from django_q.tasks import async_iter
from pagedown.widgets import AdminPagedownWidget

from zzr_mailer.content.models import Article, Journal, News
from zzr_mailer.content.news_sources import Zzr

from .models import AddressBook, IssueAnnouncementLetter, NewsDigestLetter


@admin.register(AddressBook)
class AddressBookAdmin(DjangoObjectActions, admin.ModelAdmin):
    def load_from_sendpulse(modeladmin, request, queryset):
        AddressBook.load_from_sendpulse()

    load_from_sendpulse.label = "Загрузить из Sendpulse"

    changelist_actions = ("load_from_sendpulse",)


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
        url = reverse("letter:newsdigest_detail", args=[obj.id])
        return format_html(f"<a href='{url}'>Просмотр</a>")

    detail_view.short_description = "Ссылка"

    def create_campaign(self, obj):
        obj.update_status()

        if obj.status == NewsDigestLetter.Status.UNPLANNED:
            url = reverse("letter:newsdigest_create_campaign", args=[obj.id])
            text = "Запланировать рассылку"
        elif obj.status == NewsDigestLetter.Status.PENDING:
            url = "#"
            text = ""
        elif obj.status == NewsDigestLetter.Status.SENT:
            url = "#"
            text = ""
        elif obj.status == NewsDigestLetter.Status.PLANNED:
            url = reverse("letter:newsdigest_cancel_campaign", args=[obj.id])
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
class IssueAnnouncementLetterAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }
    inlines = (
        IssueAnnouncementLetterArticlesLongInline,
        IssueAnnouncementLetterArticlesShortInline,
    )
    list_display = (
        "title",
        "send_date",
        "detail_view",
        "status",
        "create_campaign",
    )

    fields = (
        "journal",
        "title",
        "greeting",
        "advertisement",
        "send_date",
        "addressbooks",
    )

    def detail_view(self, obj):
        url = reverse("letter:issueannouncement_detail", args=[obj.id])
        return format_html(f"<a href='{url}'>Просмотр</a>")

    detail_view.short_description = "Ссылка"

    def create_campaign(self, obj):
        obj.update_status()

        if obj.status == IssueAnnouncementLetter.Status.UNPLANNED:
            url = reverse("letter:issueannouncement_create_campaign", args=[obj.id])
            text = "Запланировать рассылку"
        elif obj.status == IssueAnnouncementLetter.Status.PENDING:
            url = "#"
            text = ""
        elif obj.status == IssueAnnouncementLetter.Status.SENT:
            url = "#"
            text = ""
        elif obj.status == IssueAnnouncementLetter.Status.PLANNED:
            url = reverse("letter:issueannouncement_cancel_campaign", args=[obj.id])
            text = "Отменить рассылку"
        elif obj.status == IssueAnnouncementLetter.Status.EXPIRED:
            url = ""
            text = ""
        elif obj.status == IssueAnnouncementLetter.Status.ERROR:
            url = ""
            text = ""
        return format_html(f"<a href='{url}'>{text}</a>")

    create_campaign.short_description = "Действия"

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
