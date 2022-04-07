from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from ..models import Letter


class AbstractLetterAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "send_date",
        "detail_view",
        "status",
        "create_campaign",
    )

    def detail_view(self, obj):
        url = reverse(f"letter:{obj.letter_type}_detail", args=[obj.id])
        return format_html(f"<a href='{url}'>Просмотр</a>")

    detail_view.short_description = "Ссылка"

    def create_campaign(self, obj):
        obj.update_status()

        if obj.status == Letter.Status.UNPLANNED:
            url = reverse(f"letter:{obj.letter_type}_create_campaign", args=[obj.id])
            text = "Запланировать рассылку"
        elif obj.status == Letter.Status.PENDING:
            url = "#"
            text = ""
        elif obj.status == Letter.Status.SENT:
            url = "#"
            text = ""
        elif obj.status == Letter.Status.PLANNED:
            url = reverse(f"letter:{obj.letter_type}_cancel_campaign", args=[obj.id])
            text = "Отменить рассылку"
        elif obj.status == Letter.Status.EXPIRED:
            url = ""
            text = ""
        elif obj.status == Letter.Status.ERROR:
            url = ""
            text = ""
        return format_html(f"<a href='{url}'>{text}</a>")

    create_campaign.short_description = "Действия"
