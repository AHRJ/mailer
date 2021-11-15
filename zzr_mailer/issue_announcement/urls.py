from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from .views import (
    IssueAnnouncementLetterCancelCampaignView,
    IssueAnnouncementLetterCreateCampaignView,
    IssueAnnouncementLetterDetailView,
    IssueAnnouncementLetterListView,
)

app_name = "issue_announcement"

urlpatterns = [
    path("", view=IssueAnnouncementLetterListView.as_view(), name="list"),
    path("<int:pk>/", view=IssueAnnouncementLetterDetailView.as_view(), name="detail"),
    path(
        "<int:pk>/create-campaign",
        view=staff_member_required(IssueAnnouncementLetterCreateCampaignView.as_view()),
        name="create_campaign",
    ),
    path(
        "<int:pk>/cancel-campaign",
        view=staff_member_required(IssueAnnouncementLetterCancelCampaignView.as_view()),
        name="cancel_campaign",
    ),
]
