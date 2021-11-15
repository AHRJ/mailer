from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from .views import (
    NewsDigestLetterCancelCampaignView,
    NewsDigestLetterCreateCampaignView,
    NewsDigestLetterDetailView,
    NewsDigestLetterListView,
)

app_name = "news_digest"
urlpatterns = [
    path("", view=NewsDigestLetterListView.as_view(), name="list"),
    path("<int:pk>/", view=NewsDigestLetterDetailView.as_view(), name="detail"),
    path(
        "<int:pk>/create-campaign",
        view=staff_member_required(NewsDigestLetterCreateCampaignView.as_view()),
        name="create_campaign",
    ),
    path(
        "<int:pk>/cancel-campaign",
        view=staff_member_required(NewsDigestLetterCancelCampaignView.as_view()),
        name="cancel_campaign",
    ),
]
