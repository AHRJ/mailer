from django.views.generic import DetailView, ListView

from ..models import NewsDigestLetter
from .abstract_views import AbstractCancelCampaignView, AbstractCreateCampaignView


class NewsDigestLetterListView(ListView):
    model = NewsDigestLetter


class NewsDigestLetterDetailView(DetailView):
    model = NewsDigestLetter


class NewsDigestLetterCreateCampaignView(AbstractCreateCampaignView):
    model = NewsDigestLetter


class NewsDigestLetterCancelCampaignView(AbstractCancelCampaignView):
    model = NewsDigestLetter
