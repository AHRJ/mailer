from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "zzr_mailer.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import zzr_mailer.users.signals  # noqa F401
        except ImportError:
            pass
