from django.views.generic import DetailView, ListView

from .models import Letter


class LetterDetailView(DetailView):
    model = Letter


class LetterListView(ListView):
    model = Letter
