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
        "id",
        "send_date",
        "link_to_detail_view",
        "create_campaign",
    )
    exclude = ("campaigns",)

    def link_to_detail_view(self, obj):
        url = reverse("news_digest:detail", args=[obj.id])
        return format_html(f"<a href='{url}'>Просмотр</a>")

    def create_campaign(self, obj):
        if not obj.campaigns.exists():
            url = reverse("news_digest:create_campaign", args=[obj.id])
            text = "Запланировать рассылку"
        else:
            url = reverse("news_digest:cancel_campaign", args=[obj.id])
            text = "Отменить рассылку"
        return format_html(f"<a href='{url}'>{text}</a>")

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
