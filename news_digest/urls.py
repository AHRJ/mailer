from django.urls import path

from .views import LetterDetailView, LoadNewsView

app_name = "news_digest"
urlpatterns = [
    path("<pk>", view=LetterDetailView.as_view(), name="detail"),
    path("update/", view=LoadNewsView.as_view(), name="update"),
]
