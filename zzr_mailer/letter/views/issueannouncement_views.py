from django.views.generic import DetailView, ListView

from ..models import IssueAnnouncementLetter
from .abstract_views import AbstractCancelCampaignView, AbstractCreateCampaignView


class IssueAnnouncementLetterDetailView(DetailView):
    model = IssueAnnouncementLetter


class IssueAnnouncementLetterListView(ListView):
    model = IssueAnnouncementLetter


class IssueAnnouncementLetterCreateCampaignView(AbstractCreateCampaignView):
    model = IssueAnnouncementLetter


class IssueAnnouncementLetterCancelCampaignView(AbstractCancelCampaignView):
    model = IssueAnnouncementLetter
