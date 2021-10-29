from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django_q.tasks import async_task

from letter.models import Campaign
from zzr_mailer.utils.sendpulse import SPSender

from .models import IssueAnnouncementLetter


class IssueAnnouncementLetterDetailView(DetailView):
    model = IssueAnnouncementLetter


class IssueAnnouncementLetterListView(ListView):
    model = IssueAnnouncementLetter


class IssueAnnouncementLetterCreateCampaignView(DetailView):
    model = IssueAnnouncementLetter

    def assign_campaigns(task):
        campaign_ids = task.result
        letter = task.kwargs.get("letter")
        try:
            campaigns = [Campaign.objects.create(id=id) for id in campaign_ids]
            letter.campaigns.add(*campaigns)
            status = IssueAnnouncementLetter.Status.PLANNED
        except:  # noqa
            status = IssueAnnouncementLetter.Status.ERROR
        finally:
            letter.status = status
            letter.save()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        letter_title = self.object.title
        letter_body = render_to_string(
            r"issue_announcement/issueannouncementletter_detail.html", context=context
        )
        letter_send_date = self.object.send_date
        letter_addresbook_ids = [entry.id for entry in self.object.addressbooks.all()]

        async_task(
            SPSender.add_campaigns,
            hook=IssueAnnouncementLetterCreateCampaignView.assign_campaigns,
            from_email="info@zzr.ru",
            from_name="ИД Животноводство",
            subject=letter_title,
            body=letter_body,
            send_date=letter_send_date,
            addressbook_ids=letter_addresbook_ids,
            letter=self.object,
        )
        self.object.status = IssueAnnouncementLetter.Status.PENDING
        self.object.save()

        return HttpResponseRedirect(
            reverse("admin:issue_announcement_issueannouncementletter_changelist")
        )


class IssueAnnouncementLetterCancelCampaignView(DetailView):
    model = IssueAnnouncementLetter

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        letter_campaign_ids = [entry.id for entry in self.object.campaigns.all()]
        SPSender.cancel_campaigns(letter_campaign_ids)
        self.object.campaigns.all().delete()
        self.object.status = IssueAnnouncementLetter.Status.UNPLANNED
        self.object.save()
        return HttpResponseRedirect(
            reverse("admin:issue_announcement_issueannouncementletter_changelist")
        )