from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from .views import (
    LetterCancelCampaignView,
    LetterCreateCampaignView,
    LetterDetailView,
    LetterListView,
)

app_name = "news_digest"
urlpatterns = [
    path("", view=LetterListView.as_view(), name="list"),
    path("<int:pk>/", view=LetterDetailView.as_view(), name="detail"),
    path(
        "<int:pk>/create-campaign",
        view=staff_member_required(LetterCreateCampaignView.as_view()),
        name="create_campaign",
    ),
    path(
        "<int:pk>/cancel-campaign",
        view=staff_member_required(LetterCancelCampaignView.as_view()),
        name="cancel_campaign",
    ),
]
