from django.contrib import admin
from django_object_actions import DjangoObjectActions

from zzr_mailer.content.news_sources import Zzr

from .models import Advertisement, AdvertisementBanner, Article, Journal, News


@admin.register(News)
class NewsAdmin(DjangoObjectActions, admin.ModelAdmin):
    def load_from_zzr(modeladmin, request, queryset):
        News.load_from(Zzr)

    load_from_zzr.label = "Загрузить из zzr.ru"

    list_display = ("title", "pub_date")
    exclude = ("uuid", "image_url")
    ordering = ("-pub_date",)
    changelist_actions = ("load_from_zzr",)


@admin.register(Article)
class ArticleAdmin(DjangoObjectActions, admin.ModelAdmin):
    def load_from_zzr(modeladmin, request, queryset):
        Article.load_from(Zzr)

    load_from_zzr.label = "Загрузить из zzr.ru"
    list_display = ("title", "id")
    ordering = ("-created",)
    changelist_actions = ("load_from_zzr",)


@admin.register(Journal)
class JournalAdmin(DjangoObjectActions, admin.ModelAdmin):
    def is_pdf_uploaded(obj):
        return True if obj.pdf else False

    def load_from_zzr(modeladmin, request, queryset):
        Journal.load_from(Zzr)

    is_pdf_uploaded.short_description = "PDF"
    is_pdf_uploaded.boolean = True
    load_from_zzr.label = "Загрузить из zzr.ru"

    list_display = ("issue", "year", is_pdf_uploaded)
    ordering = ("-created",)
    exclude = ("issue_type",)
    changelist_actions = ("load_from_zzr",)


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    pass


@admin.register(AdvertisementBanner)
class AdvertisementBannerAdmin(admin.ModelAdmin):
    pass
