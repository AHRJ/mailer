# Generated by Django 3.1.12 on 2022-03-11 15:52

from django.db import migrations, models
import zzr_mailer.content.models.journal


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0005_auto_20220304_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='pdf',
            field=models.FileField(blank=True, upload_to=zzr_mailer.content.models.journal.Journal.content_file_name, verbose_name='PDF'),
        ),
    ]
