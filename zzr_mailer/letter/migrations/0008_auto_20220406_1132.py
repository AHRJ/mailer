# Generated by Django 3.1.12 on 2022-04-06 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('letter', '0007_generictletter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genericletter',
            options={'verbose_name': 'Обычное письмо', 'verbose_name_plural': 'Обычные письма'},
        ),
    ]
