# Generated by Django 3.1.12 on 2023-11-22 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letter', '0013_auto_20231122_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericletter',
            name='campaign_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='issueannouncementletter',
            name='campaign_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='issuedownloadletter',
            name='campaign_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='newsdigestletter',
            name='campaign_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
