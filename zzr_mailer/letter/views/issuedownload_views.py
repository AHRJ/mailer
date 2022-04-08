from django.views.generic import DetailView

from zzr_mailer.content.models import Journal

from ..models import IssueDownloadLetter
from .abstract_views import AbstractCancelCampaignView, AbstractCreateCampaignView


class IssueDownloadLetterDetailView(DetailView):
    model = IssueDownloadLetter

    def get_context_data(self, **kwargs):
        context = super(IssueDownloadLetterDetailView, self).get_context_data(**kwargs)
        context["additional_journals"] = Journal.objects.filter(
            year=self.object.journal.year
        ).exclude(pk=self.object.journal.pk)
        return context


class IssueDownloadLetterCreateCampaignView(AbstractCreateCampaignView):
    model = IssueDownloadLetter

    def get_context_data(self, **kwargs):
        context = super(IssueDownloadLetterCreateCampaignView, self).get_context_data(
            **kwargs
        )
        context["additional_journals"] = Journal.objects.filter(
            year=self.object.journal.year
        ).exclude(pk=self.object.journal.pk)
        return context


class IssueDownloadLetterCancelCampaignView(AbstractCancelCampaignView):
    model = IssueDownloadLetter
