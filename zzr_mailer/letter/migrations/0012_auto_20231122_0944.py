# Generated by Django 3.1.12 on 2023-11-22 09:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('letter', '0011_issueannouncementletter_advertisement_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericletter',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='issueannouncementletter',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='issuedownloadletter',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.AddField(
            model_name='newsdigestletter',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
