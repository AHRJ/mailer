# Generated by Django 3.1.12 on 2021-07-07 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news_digest', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='letter',
            old_name='pub_date',
            new_name='send_date',
        ),
    ]
