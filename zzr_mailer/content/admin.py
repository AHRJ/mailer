from django.contrib import admin

from .models import Advertisement, Article, Journal, News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("pub_date", "title")
    exclude = ("uuid", "image_url")
    ordering = ("-pub_date",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    ordering = ("-created",)


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    ordering = ("-created",)


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    pass