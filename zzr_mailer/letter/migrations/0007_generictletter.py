# Generated by Django 3.1.12 on 2022-03-30 17:10

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import zzr_mailer.letter.models.letter
import zzr_mailer.utils.utils


class Migration(migrations.Migration):

    dependencies = [
        ('letter', '0006_issuedownloadletter'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericLetter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(default='🐄 ', max_length=255, verbose_name='Тема письма')),
                ('send_date', models.DateTimeField(default=zzr_mailer.utils.utils.next_monday, verbose_name='Дата отправки')),
                ('status', models.CharField(choices=[('UNP', 'Не запланирована'), ('PND', 'Обработка...'), ('PLA', 'Запланирована'), ('SNT', 'Отправлена'), ('EXP', 'Просрочена'), ('ERR', 'Ошибка')], default='UNP', max_length=3, verbose_name='Статус')),
                ('body', models.TextField(verbose_name='Текст письма')),
                ('addressbooks', models.ManyToManyField(blank=True, default=zzr_mailer.letter.models.letter.get_active_addressbooks, to='letter.AddressBook', verbose_name='Адресные книги')),
                ('campaigns', models.ManyToManyField(blank=True, to='letter.Campaign')),
            ],
            options={
                'verbose_name': 'Базовое письмо',
                'verbose_name_plural': 'Базовые письма',
            },
        ),
    ]
