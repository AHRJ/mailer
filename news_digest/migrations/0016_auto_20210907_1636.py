# Generated by Django 3.1.12 on 2021-09-07 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20210907_1326'),
        ('news_digest', '0015_auto_20210813_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='news_long',
            field=models.ManyToManyField(related_name='_letter_news_long_+', through='news_digest.LetterNewsLong', to='content.News'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='news_short',
            field=models.ManyToManyField(related_name='_letter_news_short_+', through='news_digest.LetterNewsShort', to='content.News'),
        ),
        migrations.AlterField(
            model_name='letternewslong',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.news'),
        ),
        migrations.AlterField(
            model_name='letternewsshort',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.news'),
        ),
    ]
