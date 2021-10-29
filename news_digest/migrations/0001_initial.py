# Generated by Django 3.1.12 on 2021-10-13 20:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import letter.models.letter
import model_utils.fields
import news_digest.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('letter', '0001_initial'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Рекламный блок', max_length=255)),
                ('body', models.TextField()),
            ],
            options={
                'verbose_name': 'Рекламный блок',
                'verbose_name_plural': 'Рекламные блоки',
            },
        ),
        migrations.CreateModel(
            name='LetterNewsLong',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Новость с анонсом',
                'verbose_name_plural': 'Новости с анонсом',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='LetterNewsShort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': "Новость 'Одной строкой'",
                'verbose_name_plural': "Новости 'Одной строкой'",
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='NewsDigestLetter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(default='🐄 Новости животноводства', max_length=255, verbose_name='Тема письма')),
                ('send_date', models.DateTimeField(default=news_digest.utils.next_monday, verbose_name='Дата отправки')),
                ('status', models.CharField(choices=[('UNP', 'Не запланирована'), ('PND', 'Обработка...'), ('PLA', 'Запланирована'), ('SNT', 'Отправлена'), ('EXP', 'Просрочена'), ('ERR', 'Ошибка')], default='UNP', max_length=3, verbose_name='Статус')),
                ('subtitle', models.CharField(default='Актуальные новости отрасли', max_length=255, verbose_name='Заголовок письма')),
                ('addressbooks', models.ManyToManyField(blank=True, default=letter.models.letter.get_active_addressbooks, to='letter.AddressBook', verbose_name='Адресные книги')),
                ('advertisement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='news_digest.advertisement', verbose_name='Рекламный блок')),
                ('campaigns', models.ManyToManyField(blank=True, to='letter.Campaign')),
                ('news_long', models.ManyToManyField(related_name='_newsdigestletter_news_long_+', through='news_digest.LetterNewsLong', to='content.News')),
                ('news_short', models.ManyToManyField(related_name='_newsdigestletter_news_short_+', through='news_digest.LetterNewsShort', to='content.News')),
            ],
            options={
                'verbose_name': 'Рассылочное письмо',
                'verbose_name_plural': 'Рассылочные письма',
            },
        ),
        migrations.AddField(
            model_name='letternewsshort',
            name='letter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_digest.newsdigestletter'),
        ),
        migrations.AddField(
            model_name='letternewsshort',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.news'),
        ),
        migrations.AddField(
            model_name='letternewslong',
            name='letter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_digest.newsdigestletter'),
        ),
        migrations.AddField(
            model_name='letternewslong',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.news'),
        ),
    ]
