from django.urls import path

from .views import LetterDetailView, LoadNewsView

app_name = "news_digest"
urlpatterns = [
    path("<int:pk>", view=LetterDetailView.as_view(), name="detail"),
    path("load-news/", view=LoadNewsView.as_view(), name="load_news"),
]
