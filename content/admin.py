from django.contrib import admin

from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("pub_date", "title")
    exclude = ("uuid", "image_url")
    ordering = ("-pub_date",)
