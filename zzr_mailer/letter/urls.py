from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from .views import (
    IssueAnnouncementLetterCancelCampaignView,
    IssueAnnouncementLetterCreateCampaignView,
    IssueAnnouncementLetterDetailView,
    IssueAnnouncementLetterListView,
    IssueDownloadLetterCancelCampaignView,
    IssueDownloadLetterCreateCampaignView,
    IssueDownloadLetterDetailView,
    NewsDigestLetterCancelCampaignView,
    NewsDigestLetterCreateCampaignView,
    NewsDigestLetterDetailView,
    NewsDigestLetterListView,
)

app_name = "letter"
urlpatterns = [
    path(
        "newsdigest/", view=NewsDigestLetterListView.as_view(), name="newsdigest_list"
    ),
    path(
        "newsdigest/<int:pk>/",
        view=NewsDigestLetterDetailView.as_view(),
        name="newsdigestletter_detail",
    ),
    path(
        "newsdigest/<int:pk>/create-campaign/",
        view=staff_member_required(NewsDigestLetterCreateCampaignView.as_view()),
        name="newsdigestletter_create_campaign",
    ),
    path(
        "newsdigest/<int:pk>/cancel-campaign/",
        view=staff_member_required(NewsDigestLetterCancelCampaignView.as_view()),
        name="newsdigestletter_cancel_campaign",
    ),
    path(
        "issue-announcement/",
        view=IssueAnnouncementLetterListView.as_view(),
        name="issueannouncementletter_list",
    ),
    path(
        "issue-announcement/<int:pk>/",
        view=IssueAnnouncementLetterDetailView.as_view(),
        name="issueannouncementletter_detail",
    ),
    path(
        "issue-announcement/<int:pk>/create-campaign/",
        view=staff_member_required(IssueAnnouncementLetterCreateCampaignView.as_view()),
        name="issueannouncementletter_create_campaign",
    ),
    path(
        "issue-announcement/<int:pk>/cancel-campaign/",
        view=staff_member_required(IssueAnnouncementLetterCancelCampaignView.as_view()),
        name="issueannouncementletter_cancel_campaign",
    ),
    path(
        "issue-download/<int:pk>/",
        view=IssueDownloadLetterDetailView.as_view(),
        name="issuedownloadletter_detail",
    ),
    path(
        "issue-download/<int:pk>/create-campaign/",
        view=staff_member_required(IssueDownloadLetterCreateCampaignView.as_view()),
        name="issuedownloadletter_create_campaign",
    ),
    path(
        "issue-download/<int:pk>/cancel-campaign/",
        view=staff_member_required(IssueDownloadLetterCancelCampaignView.as_view()),
        name="issuedownloadletter_cancel_campaign",
    ),
]
