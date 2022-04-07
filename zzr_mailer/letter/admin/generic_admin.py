from django.contrib import admin
from django.db import models
from pagedown.widgets import AdminPagedownWidget

from ..models import GenericLetter
from .abstract_admin import AbstractLetterAdmin


@admin.register(GenericLetter)
class GenericLetterAdmin(AbstractLetterAdmin):

    formfield_overrides = {
        models.TextField: {"widget": AdminPagedownWidget},
    }

    fields = (
        "title",
        "body",
        "send_date",
        "addressbooks",
    )
