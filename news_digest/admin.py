from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import AddressBook, Advertisement, Letter, News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("pub_date", "title")
    exclude = ("uuid", "image_url")
    ordering = ("-pub_date",)


class LetterNewsLongInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Letter.news_long.through
    extra = 8


class LetterNewsShortInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Letter.news_short.through
    extra = 10


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    pass


@admin.register(AddressBook)
class AddressBookAdmin(admin.ModelAdmin):
    pass


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    inlines = (
        LetterNewsLongInline,
        LetterNewsShortInline,
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
        if obj.status == Letter.Status.UNPLANNED:
            url = reverse("news_digest:create_campaign", args=[obj.id])
            text = "Запланировать рассылку"
        elif obj.status == Letter.Status.PENDING:
            url = "#"
            text = ""
        elif obj.status == Letter.Status.SENT:
            url = "#"
            text = ""
        elif obj.status == Letter.Status.PLANNED:
            url = reverse("news_digest:cancel_campaign", args=[obj.id])
            text = "Отменить рассылку"
        elif obj.status == Letter.Status.EXPIRED:
            url = ""
            text = ""
        return format_html(f"<a href='{url}'>{text}</a>")

    create_campaign.short_description = "Действия"

    def add_view(self, request, form_url="", extra_context=None):
        News.load_from_zzr()
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        News.load_from_zzr()
        return super().change_view(request, object_id, form_url, extra_context)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for n in form.instance.news_long.all():
            n.load_img_from_url()
