from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView, ListView

from .models import Letter, News


class LetterDetailView(DetailView):
    model = Letter


class LetterListView(ListView):
    model = Letter


class LoadNewsView(View):
    def get(self, request):
        response_status = News.load_from_zzr()
        return (
            HttpResponse("OK")
            if response_status == 200
            else HttpResponse("Error " + str(response_status))
        )
