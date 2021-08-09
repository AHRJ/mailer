import base64
import logging
import os
import time
from hashlib import md5

import memcache
import requests
from django.conf import settings

try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        try:
            from django.utils import simplejson as json
        except ImportError:
            raise ImportError("A json library is required to use this python library")

logger = logging.getLogger(__name__)
logger.propagate = False
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter("%(levelname)-8s [%(asctime)s]  %(message)s"))
logger.addHandler(ch)


class SPSenderError(Exception):
    def __init__(self, message=""):
        self.message = message


class PySendPulse:
    """SendPulse REST API python wrapper"""

    __api_url = "https://api.sendpulse.com"
    __user_id = None
    __secret = None
    __token = None
    __token_file_path = ""
    __token_hash_name = None
    __storage_type = "FILE"
    __refresh_token = 0
    __memcached_host = "127.0.0.1:11211"
    __name__ = "PySendPulse"

    MEMCACHED_VALUE_TIMEOUT = 3600
    ALLOWED_STORAGE_TYPES = ["FILE", "MEMCACHED"]

    def __init__(
        self,
        user_id,
        secret,
        storage_type="FILE",
        token_file_path="",
        memcached_host="127.0.0.1:11211",
    ):
        """SendPulse API constructor
        @param user_id: string REST API ID from SendPulse settings
        @param secret: string REST API Secret from SendPulse settings
        @param storage_type: string FILE|MEMCACHED
        @param memcached_host: string Host for Memcached server, default is 127.0.0.1:11211
        @raise: Exception empty credentials or get token failed
        """
        logger.info("Initialization SendPulse REST API Class")
        if not user_id or not secret:
            raise Exception("Empty ID or SECRET")

        self.__user_id = user_id
        self.__secret = secret
        self.__storage_type = storage_type.upper()
        self.__token_file_path = token_file_path
        self.__memcached_host = memcached_host
        m = md5()
        m.update("{}::{}".format(user_id, secret).encode("utf-8"))
        self.__token_hash_name = m.hexdigest()
        if self.__storage_type not in self.ALLOWED_STORAGE_TYPES:
            logger.warning(
                "Wrong storage type '{}'. Allowed storage types are: {}".format(
                    storage_type, self.ALLOWED_STORAGE_TYPES
                )
            )
            logger.warning("Try to use 'FILE' instead.")
            self.__storage_type = "FILE"
        logger.debug(
            "Try to get security token from '{}'".format(
                self.__storage_type,
            )
        )
        if self.__storage_type == "MEMCACHED":
            mc = memcache.Client([self.__memcached_host])
            self.__token = mc.get(self.__token_hash_name)
        else:  # file
            filepath = "{}{}".format(self.__token_file_path, self.__token_hash_name)
            if os.path.isfile(filepath):
                with open(filepath, "rb") as f:
                    self.__token = f.readline()

            else:
                logger.error(
                    "Can't find file '{}' to read security token.".format(filepath)
                )
        logger.debug(
            "Got: '{}'".format(
                self.__token,
            )
        )
        if not self.__token and not self.__get_token():
            raise Exception(
                "Could not connect to API. Please, check your ID and SECRET"
            )

    def __get_token(self):
        """Get new token from API server and store it in storage
        @return: boolean
        """
        logger.debug("Try to get new token from server")
        self.__refresh_token += 1
        data = {
            "grant_type": "client_credentials",
            "client_id": self.__user_id,
            "client_secret": self.__secret,
        }
        response = self.__send_request("oauth/access_token", "POST", data, False)
        if response.status_code != 200:
            return False
        self.__refresh_token = 0
        self.__token = response.json()["access_token"]
        logger.debug(
            "Got: '{}'".format(
                self.__token,
            )
        )
        if self.__storage_type == "MEMCACHED":
            logger.debug(
                "Try to set token '{}' into 'MEMCACHED'".format(
                    self.__token,
                )
            )
            mc = memcache.Client([self.__memcached_host])
            mc.set(self.__token_hash_name, self.__token, self.MEMCACHED_VALUE_TIMEOUT)
        else:
            filepath = "{}{}".format(self.__token_file_path, self.__token_hash_name)
            try:
                if not os.path.isdir(self.__token_file_path):
                    os.makedirs(self.__token_file_path, exist_ok=True)

                with open(filepath, "w") as f:
                    f.write(self.__token)
                    logger.debug(
                        "Set token '{}' into 'FILE' '{}'".format(self.__token, filepath)
                    )
            except IOError:
                logger.warning(
                    "Can't create 'FILE' to store security token. Please, check your settings."
                )
        if self.__token:
            return True
        return False

    def __send_request(
        self,
        path,
        method="GET",
        params=None,
        use_token=True,
        use_json_content_type=False,
    ):
        """Form and send request to API service
        @param path: sring what API url need to call
        @param method: HTTP method GET|POST|PUT|DELETE
        @param params: dict argument need to send to server
        @param use_token: boolean need to use token or not
        @param use_json_content_type: boolean need to convert params data to json or not
        @return: HTTP requests library object http://www.python-requests.org/
        """
        url = "{}/{}".format(self.__api_url, path)
        method.upper()
        logger.debug(
            "__send_request method: {} url: '{}' with parameters: {}".format(
                method, url, params
            )
        )
        if type(params) not in (dict, list):
            params = {}
        if use_token and self.__token:
            headers = {"Authorization": "Bearer {}".format(self.__token)}
        else:
            headers = {}
        if use_json_content_type and params:
            headers["Content-Type"] = "application/json"
            params = json.dumps(params)

        if method == "POST":
            response = requests.post(url, headers=headers, data=params)
        elif method == "PUT":
            response = requests.put(url, headers=headers, data=params)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, data=params)
        else:
            response = requests.get(url, headers=headers, params=params)
        if response.status_code == 401 and self.__refresh_token == 0:
            self.__get_token()
            return self.__send_request(path, method, params)
        elif response.status_code == 404:
            logger.warning(
                "404: Sorry, the page you are looking for could not be found."
            )
            logger.debug(
                "Raw_server_response: {}".format(
                    response.text,
                )
            )
        elif response.status_code == 500:
            logger.critical(
                "Whoops, looks like something went wrong on the server.\
                 Please contact with out support tech@sendpulse.com."
            )
        else:
            try:
                logger.debug(
                    "Request response: {}".format(
                        response.json(),
                    )
                )
            except:  # noqa
                logger.critical(
                    "Raw server response: {}".format(
                        response.text,
                    )
                )
        return response

    def __handle_result(self, data):
        """Process request results
        @param data:
        @return: dictionary with response message and/or http code
        """
        if "status_code" not in data:
            if data.status_code == 200:
                logger.debug(
                    "Hanle result: {}".format(
                        data.json(),
                    )
                )
                return data.json()
            elif data.status_code == 404:
                response = {
                    "is_error": True,
                    "http_code": data.status_code,
                    "message": "Sorry, the page you are looking for {} could not be found.".format(
                        data.url,
                    ),
                }
            elif data.status_code == 500:
                response = {
                    "is_error": True,
                    "http_code": data.status_code,
                    "message": "Whoops, looks like something went wrong on the server.\
                                Please contact with out support tech@sendpulse.com.",
                }
            else:
                response = {"is_error": True, "http_code": data.status_code}
                response.update(data.json())
        else:
            response = {"is_error": True, "http_code": data}
        logger.debug(
            "Hanle result: {}".format(
                response,
            )
        )
        return {"data": response}

    def __handle_error(self, custom_message=None):
        """Process request errors
        @param custom_message:
        @return: dictionary with response custom error message and/or error code
        """
        message = {"is_error": True}
        if custom_message is not None:
            message["message"] = custom_message
        logger.error(
            "Hanle error: {}".format(
                message,
            )
        )
        return message

    # ------------------------------------------------------------------ #
    #                             BALANCE                                #
    # ------------------------------------------------------------------ #

    def get_balance(self, currency=None):
        """Get balance
        @param currency: USD, EUR, GBP, UAH, RUR, INR, JPY
        @return: dictionary with response message
        """
        logger.info("Function call: get_balance")
        return self.__handle_result(
            self.__send_request(
                "balance/{}".format(currency.upper() if currency else ""),
            )
        )

    # ------------------------------------------------------------------ #
    #                           ADDRESSBOOKS                             #
    # ------------------------------------------------------------------ #

    def add_addressbook(self, addressbook_name):
        """Create addressbook
        @param addressbook_name: string name for addressbook
        @return: dictionary with response message
        """
        logger.info(
            "Function call: create_addressbook: '{}'".format(
                addressbook_name,
            )
        )
        return (
            self.__handle_error("Empty AddressBook name")
            if not addressbook_name
            else self.__handle_result(
                self.__send_request(
                    "addressbooks", "POST", {"bookName": addressbook_name}
                )
            )
        )

    def edit_addressbook(self, id, new_addressbook_name):
        """Edit addressbook name
        @param id: unsigned int addressbook ID
        @param new_addressbook_name: string new name for addressbook
        @return: dictionary with response message
        """
        logger.info(
            "Function call: edit_addressbook: '{}' with new addressbook name '{}'".format(
                id, new_addressbook_name
            )
        )
        if not id or not new_addressbook_name:
            return self.__handle_error("Empty new name or addressbook id")
        return self.__handle_result(
            self.__send_request(
                "addressbooks/{}".format(id), "PUT", {"name": new_addressbook_name}
            )
        )

    def delete_addressbook(self, id):
        """Remove addressbook
        @param id: unsigned int addressbook ID
        @return: dictionary with response message
        """
        logger.info(
            "Function call: remove_addressbook: '{}'".format(
                id,
            )
        )
        return (
            self.__handle_error("Empty addressbook id")
            if not id
            else self.__handle_result(
                self.__send_request("addressbooks/{}".format(id), "DELETE")
            )
        )

    def get_list_of_addressbooks(self, limit=0, offset=0):
        """Get list of addressbooks
        @param limit: unsigned int max limit of records. The max value is 100
        @param offset: unsigned int how many records pass before selection
        @return: dictionary with response message
        """
        logger.info("Function call: get_list_of_addressbooks")
        return self.__handle_result(
            self.__send_request(
                "addressbooks", "GET", {"limit": limit or 0, "offset": offset or 0}
            )
        )

    def get_addressbook_info(self, id):
        """Get information about addressbook
        @param id: unsigned int addressbook ID
        @return: dictionary with response message
        """
        logger.info(
            "Function call: get_addressbook_info: '{}'".format(
                id,
            )
        )
        return (
            self.__handle_error("Empty addressbook id")
            if not id
            else self.__handle_result(self.__send_request("addressbooks/{}".format(id)))
        )

    def get_addressbook_variables(self, id):
        """Get a list of variables available on a mailing list
        @param id: unsigned int addressbook ID
        @return: list with variables of addressbook
        """
        logger.info(
            "Function call: get_addressbook_variables_list: '{}'".format(
                id,
            )
        )
        return (
            self.__handle_error("Empty addressbook id")
            if not id
            else self.__handle_result(
                self.__send_request("addressbooks/{}/variables".format(id))
            )
        )

    # ------------------------------------------------------------------ #
    #                        EMAIL  ADDRESSES                            #
    # ------------------------------------------------------------------ #

    def get_emails_from_addressbook(self, id, limit=0, offset=0):
        """List email addresses from addressbook
        @param id: unsigned int addressbook ID
        @param limit: unsigned int max limit of records. The max value is 100
        @param offset: unsigned int how many records pass before selection
        @return: dictionary with response message
        """
        logger.info(
            "Function call: get_emails_from_addressbook: '{}'".format(
                id,
            )
        )
        return (
            self.__handle_error("Empty addressbook id")
            if not id
            else self.__handle_result(
                self.__send_request(
                    "addressbooks/{}/emails".format(id),
                    "GET",
                    {"limit": limit or 0, "offset": offset or 0},
                )
            )
        )

    def add_emails_to_addressbook(self, id, emails):
        """Add new emails to addressbook
        @param id: unsigned int addressbook ID
        @param emails: list of dictionaries [
                {'email': 'test@test.com', 'variables': {'varname_1': 'value_1', ..., 'varname_n': 'value_n' }},
                {...},
                {'email': 'testn@testn.com'}}
            ]
        @return: dictionary with response message
        """
        logger.info(
            "Function call: add_emails_to_addressbook into: {}".format(
                id,
            )
        )
        if not id or not emails:
            self.__handle_error("Empty addressbook id or emails")
        try:
            emails = json.dumps(emails)
        except:  # noqa
            logger.debug("Emails: {}".format(emails))
            return self.__handle_error("Emails list can't be converted by JSON library")
        return self.__handle_result(
            self.__send_request(
                "addressbooks/{}/emails".format(id), "POST", {"emails": emails}
            )
        )

    def delete_emails_from_addressbook(self, id, emails):
        """Delete email addresses from addressbook
        @param id: unsigned int addressbook ID
        @param emails: list of emails ['test_1@test_1.com', ..., 'test_n@test_n.com']
        @return: dictionary with response message
        """
        logger.info(
            "Function call: delete_emails_from_addressbook from: {}".format(
                id,
            )
        )
        if not id or not emails:
            self.__handle_error("Empty addressbook id or emails")
        try:
            emails = json.dumps(emails)
        except:  # noqa
            logger.debug("Emails: {}".format(emails))
            return self.__handle_error("Emails list can't be converted by JSON library")
        return self.__handle_result(
            self.__send_request(
                "addressbooks/{}/emails".format(id), "DELETE", {"emails": emails}
            )
        )

    def get_emails_stat_by_campaigns(self, emails):
        """Get campaigns statistic for list of emails
        @param emails: list of emails ['test_1@test_1.com', ..., 'test_n@test_n.com']
        @return: dictionary with response message
        """
        logger.info("Function call: get_emails_stat_by_campaigns")
        if not emails:
            self.__handle_error("Empty emails")
        try:
            emails = json.dumps(emails)
        except:  # noqa
            logger.debug("Emails: {}".format(emails))
            return self.__handle_error("Emails list can't be converted by JSON library")
        return self.__handle_result(
            self.__send_request("emails/campaigns", "POST", {"emails": emails})
        )

    def set_variables_for_email(self, id, email, variables):
        """Set variables for email
        @param id: unsigned int addressbook ID
        @param email: string
        @param variables: dictionary
        @return: dictionary with response message
        """
        logger.info(
            "Function call: set_variables_for_email: '{}' with email: '{}' new variables: '{}'".format(
                id, email, variables
            )
        )
        return (
            self.__handle_error("Empty addressbook id")
            if not id
            else self.__handle_result(
                self.__send_request(
                    "addressbooks/{}/emails/variable".format(id),
                    "POST",
                    {"email": email, "variables": variables},
                    True,
                    True,
                )
            )
        )

    # ------------------------------------------------------------------ #
    #                        EMAIL  CAMPAIGNS                            #
    # ------------------------------------------------------------------ #

    def get_campaign_cost(self, id):
        """Get cost of campaign based on addressbook
        @param id: unsigned int addressbook ID
        @return: dictionary with response message
        """
        logger.info(
            "Function call: get_campaign_cost: '{}'".format(
                id,
            )
        )
        return (
            self.__handle_error("Empty addressbook id")
            if not id
            else self.__handle_result(
                self.__send_request("addressbooks/{}/cost".format(id))
            )
        )

    def get_list_of_campaigns(self, limit=0, offset=0):
        """Get list of campaigns
        @param limit: unsigned int max limit of records. The max value is 100
        @param offset: unsigned int how many records pass before selection
        @return: dictionary with response message
        """
        logger.info("Function call: get_list_of_campaigns")
        return self.__handle_result(
            self.__send_request(
                "campaigns", "GET", {"limit": limit or 0, "offset": offset or 0}
            )
        )

    def get_campaign_info(self, id):
        """Get information about campaign
        @param id: unsigned int campaign ID
        @return: dictionary with response message
        """
        logger.info(
            "Function call: get_campaign_info from: {}".format(
                id,
            )
        )
        return (
            self.__handle_error("Empty campaign id")
            if not id
            else self.__handle_result(
                self.__send_request(
                    "campaigns/{}".format(
                        id,
                    )
                )
            )
        )

    def get_campaign_stat_by_countries(self, id):
        """Get information about campaign
        @param id: unsigned int campaign ID
        @return: dictionary with response message
        """
        logger.info(
            "Function call: get_campaign_stat_by_countries from: '{}'".format(
                id,
            )
        )
        return (
            self.__handle_error("Empty campaign id")
            if not id
            else self.__handle_result(
                self.__send_request(
                    "campaigns/{}/countries".format(
                        id,
                    )
                )
            )
        )

    def get_campaign_stat_by_referrals(self, id):
        """Get campaign statistic by referrals
        @param id: unsigned int campaign ID
        @return: dictionary with response message
        """
        logger.info(
            "Function call: get_campaign_stat_by_referrals from: '{}'".format(
                id,
            )
        )
        return (
            self.__handle_error("Empty campaign id")
            if not id
            else self.__handle_result(
                self.__send_request(
                    "campaigns/{}/referrals".format(
                        id,
                    )
                )
            )
        )

    def add_campaign(
        self,
        from_email,
        from_name,
        subject,
        body,
        addressbook_id,
        campaign_name="",
        send_date="",
        attachments=None,
    ):
        """Create new campaign
        @param from_email: string senders email
        @param from_name: string senders name
        @param subject: string campaign title
        @param body: string campaign body
        @param addressbook_id: unsigned int addressbook ID
        @param campaign_name: string campaign name
        @param send_date: date of the scheduled email campaign (Y-m-d H:i:s)
        @param attachments: dictionary with {filename_1: filebody_1, ..., filename_n: filebody_n}
        @return: dictionary with response message
        """
        logger.info("Function call: create_campaign")
        if not from_name or not from_email:
            return self.__handle_error(
                "Seems you pass not all data for sender: Email or Name"
            )
        elif not subject or not body:
            return self.__handle_error(
                "Seems you pass not all data for task: Title or Body"
            )
        elif not addressbook_id:
            return self.__handle_error("Seems you not pass addressbook ID")
        if not attachments:
            attachments = ""
        else:
            attachments = json.dumps(attachments)
        return self.__handle_result(
            self.__send_request(
                "campaigns",
                "POST",
                {
                    "sender_name": from_name,
                    "sender_email": from_email,
                    "subject": subject,
                    "body": base64.b64encode(body.encode("utf-8")),
                    "list_id": addressbook_id,
                    "name": campaign_name,
                    "send_date": send_date,
                    "attachments": attachments,
                },
            )
        )

    def cancel_campaign(self, id):
        """Cancel campaign
        @param id: unsigned int campaign ID
        @return: dictionary with response message
        """
        logger.info(
            "Function call: cancel_campaign : '{}'".format(
                id,
            )
        )
        return (
            self.__handle_error("Empty campaign id")
            if not id
            else self.__handle_result(
                self.__send_request(
                    "campaigns/{}".format(
                        id,
                    ),
                    "DELETE",
                )
            )
        )

    def add_campaigns(
        self,
        from_email,
        from_name,
        subject,
        body,
        addressbook_ids,
        campaign_name="",
        send_date="",
        attachments=None,
        **kwargs
    ):
        if not addressbook_ids:
            raise SPSenderError("No addressbooks")
            return None

        campaign_ids = []
        for addressbook_id in addressbook_ids:
            response = self.add_campaign(
                from_email=from_email,
                from_name=from_name,
                subject=subject,
                body=body,
                addressbook_id=addressbook_id,
                campaign_name=campaign_name,
                send_date=send_date,
                attachments=attachments,
            )
            try:
                campaign_id = response["id"]
                campaign_ids.append(campaign_id)
            except KeyError:
                self.cancel_campaigns(campaign_ids)
                raise SPSenderError("Обратитесь к администратору")
                return None
        return campaign_ids

    def cancel_campaigns(self, ids, **kwargs):
        for id in ids:
            result = self.cancel_campaign(id)
            logger.info(result)
            try:
                if result["result"]:
                    pass
            except KeyError:
                time.sleep(3)
                result = self.cancel_campaign(id)
                logger.info(result)


SPSender = PySendPulse(
    settings.SENDPULSE_REST_API_ID,
    settings.SENDPULSE_REST_API_SECRET,
    settings.SENDPULSE_TOKEN_STORAGE,
    memcached_host=settings.SENDPULSE_MEMCACHED_HOST,
)
