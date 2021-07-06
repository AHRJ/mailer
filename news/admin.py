from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Letter, News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    exclude = ("uuid", "image_url")
    ordering = ("-pub_date",)


class LetterNewsLongInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Letter.news_long.through
    extra = 1


class LetterNewsShortInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Letter.news_short.through
    extra = 1


@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    inlines = (
        LetterNewsLongInline,
        LetterNewsShortInline,
    )
    list_display = ("title", "id", "pub_date", "link_to_detail_view")

    def link_to_detail_view(self, obj):
        url = reverse("news:detail", args=[obj.id])
        return format_html(f"<a href='{url}' target='_blank'>Просмотр</a>")

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for n in form.instance.news_long.all():
            n.load_img_from_url()
