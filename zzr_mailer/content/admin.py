from django.contrib import admin

from .models import Advertisement, AdvertisementBanner, Article, Journal, News


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
    def is_pdf_uploaded(obj):
        return True if obj.pdf else False

    is_pdf_uploaded.short_description = "PDF"
    is_pdf_uploaded.boolean = True

    list_display = ("issue", "year", is_pdf_uploaded)
    ordering = ("-created",)
    exclude = ("issue_type",)


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    pass


@admin.register(AdvertisementBanner)
class AdvertisementBannerAdmin(admin.ModelAdmin):
    pass
