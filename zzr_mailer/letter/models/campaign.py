from django.db import models


class Campaign(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
