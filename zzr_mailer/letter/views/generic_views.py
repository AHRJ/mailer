from django.views.generic import DetailView

from ..models import GenericLetter
from .abstract_views import AbstractCancelCampaignView, AbstractCreateCampaignView


class GenericLetterDetailView(DetailView):
    model = GenericLetter


class GenericLetterCreateCampaignView(AbstractCreateCampaignView):
    model = GenericLetter


class GenericLetterCancelCampaignView(AbstractCancelCampaignView):
    model = GenericLetter
