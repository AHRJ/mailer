# Generated by Django 3.1.12 on 2021-07-08 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news_digest', '0006_auto_20210707_1710'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advertisement',
            options={'verbose_name': 'Рекламный блок', 'verbose_name_plural': 'Рекламные блоки'},
        ),
        migrations.AlterModelOptions(
            name='letter',
            options={'verbose_name': 'Рассылочное письмо', 'verbose_name_plural': 'Рассылочные письма'},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'Новость', 'verbose_name_plural': 'Новости'},
        ),
        migrations.AlterField(
            model_name='letter',
            name='advertisement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='news_digest.advertisement', verbose_name='Рекламный блок'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='subtitle',
            field=models.CharField(default='Актуальные новости отрасли', max_length=255, verbose_name='Заголовок письма'),
        ),
        migrations.AlterField(
            model_name='letter',
            name='title',
            field=models.CharField(default='🐄 Новости животноводства', max_length=255, verbose_name='Тема письма'),
        ),
    ]
