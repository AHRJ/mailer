from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import DetailView

from zzr_mailer.letter.models import Campaign
from zzr_mailer.utils.dashamail import Dashamail

from ..models import Letter


class AbstractCreateCampaignView(DetailView):
    def assign_campaigns(task):
        campaign_ids = task.result
        letter = task.kwargs.get("letter")
        try:
            campaigns = [Campaign.objects.create(id=id) for id in campaign_ids]
            letter.campaigns.add(*campaigns)
            status = Letter.Status.PLANNED
        except:  # noqa
            status = Letter.Status.ERROR
        finally:
            letter.status = status
            letter.save()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        letter_title = self.object.title
        letter_body = render_to_string(
            f"letter/{self.model.letter_type}_detail.html", context=context
        )
        letter_send_date = self.object.send_date
        letter_addresbook_ids = [
            addressbook.id for addressbook in self.object.addressbooks.all()
        ]
        letter_uuid = self.object.uuid

        try:
            campaign_id = Dashamail.add_campaign(
                from_email="info@zzr.ru",
                from_name="ИД Животноводство",
                subject=letter_title,
                html=letter_body,
                send_datetime=letter_send_date,
                list_ids=letter_addresbook_ids,
                uuid=letter_uuid,
            )
            self.object.campaign_id = campaign_id
            self.object.status = Letter.Status.PLANNED
        except:  # noqa
            self.object.status = Letter.Status.ERROR

        self.object.save()

        return HttpResponseRedirect(
            reverse(f"admin:letter_{self.model.letter_type}_changelist")
        )


class AbstractCancelCampaignView(DetailView):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        Dashamail.cancel_campaign(self.object.campaign_id)
        self.object.campaign_id = None
        self.object.status = Letter.Status.UNPLANNED
        self.object.save()
        return HttpResponseRedirect(
            reverse(f"admin:letter_{self.model.letter_type}_changelist")
        )
