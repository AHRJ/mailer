import logging

import requests
from django.conf import settings

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class DashamailAPIWrapper:

    API_KEY = settings.DASHAMAIL_API_KEY
    __name__ = "DashamailAPIWrapper"

    def get_list_of_addressbooks(self):
        r = requests.get(
            f"https://api.dashamail.ru/?method=lists.get&api_key={self.API_KEY}"
        )
        logging.info(f"Get addressbooks list from Dashamail: {r.text}")
        return r.json()["response"]["data"]

    def add_campaign(
        self,
        from_email,
        from_name,
        subject,
        html,
        list_ids,
        uuid,
        send_datetime,
    ):

        payload = {
            "api_key": self.API_KEY,
            "method": "campaigns.create",
            "list_id": str(list_ids),
            "external_campaign_id": uuid,
            "name": subject,
            "subject": subject,
            "from_name": from_name,
            "from_email": from_email,
            "html": html,
        }
        r1 = requests.post("https://api.dashamail.ru/", data=payload)
        logging.info(f"Plan a campaign with Dashamail: {r1.text}")

        campaign_id = r1.json()["response"]["data"]["campaign_id"]

        payload = {
            "api_key": self.API_KEY,
            "method": "campaigns.update",
            "campaign_id": campaign_id,
            "status": "SCHEDULE",
            "delivery_time": send_datetime,
        }
        r2 = requests.post("https://api.dashamail.ru/", data=payload)
        logging.info(f"Plan a campaign with Dashamail: {r2.text}")
        return campaign_id

    def cancel_campaign(self, campaign_id):
        payload = {
            "api_key": self.API_KEY,
            "method": "campaigns.delete",
            "campaign_id": campaign_id,
        }
        r = requests.post("https://api.dashamail.ru/", data=payload)

        logging.info(f"Cancel campaign with Dashamail: {r.text}")
        return r.json()


Dashamail = DashamailAPIWrapper()
