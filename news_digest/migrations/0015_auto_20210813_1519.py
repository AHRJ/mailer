# Generated by Django 3.1.12 on 2021-08-13 15:19

from django.db import migrations, models
import news_digest.models.letter


class Migration(migrations.Migration):

    dependencies = [
        ('news_digest', '0014_auto_20210812_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='addressbooks',
            field=models.ManyToManyField(blank=True, default=news_digest.models.letter.get_all_addressbooks, to='news_digest.AddressBook', verbose_name='Адресные книги'),
        ),
    ]
